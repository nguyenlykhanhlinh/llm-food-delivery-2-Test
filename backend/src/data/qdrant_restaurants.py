import os
import sqlite3
from uuid import uuid4
from dotenv import load_dotenv
import pandas as pd
from sqlalchemy.orm import Session
from langchain_community.vectorstores import Qdrant
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.embeddings import HuggingFaceInferenceAPIEmbeddings
from langchain_groq import ChatGroq
from langchain.schema import Document
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain
from qdrant_client import QdrantClient
from qdrant_client.models import Distance, VectorParams
from langchain.retrievers import BM25Retriever, EnsembleRetriever, ContextualCompressionRetriever
from langchain.retrievers.compressors import CrossEncoderReranker
from langchain.retrievers.rankers import HuggingFaceCrossEncoder
from langchain.prompts import ChatPromptTemplate
from langchain.chains import RunnablePassthrough, StrOutputParser

# Local imports
try:
    from data_utils import get_db, get_restaurants, get_foods
    from data_models import Restaurant, Foods
    from database import SessionLocal
except:
    from .data_utils import get_db, get_restaurants, get_foods
    from .data_models import Restaurant, Foods
    from .database import SessionLocal

RAG_SEARCH_PROMPT_TEMPLATE = """
You are an assistant helping users with their food orders based on the following context.

Context:
{context}

Question: {question}

Answer:
"""

def process_and_store_documents():
    print("Loading documents from SQLite...")
    # Kết nối database
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()

    # Lấy dữ liệu từ bảng products
    cursor.execute('SELECT id, title, content, price, category, image_urls FROM products')
    rows = cursor.fetchall()

    # Tạo documents
    documents = []
    for row in rows:
        content = f"Tiêu đề: {row[1]}\nGiá: {row[3]}\nDanh mục: {row[4]}\nMô tả: {row[2]}"
        doc = Document(
            page_content=content,
            metadata={
                "id": row[0],
                "title": row[1],
                "category": row[4],
                "image_urls": row[5]  # Thêm image_urls từ database
            }
        )
        documents.append(doc)

    conn.close()
    print(f"Loaded {len(documents)} documents")

    print("Splitting documents...")
    # Khởi tạo text splitter
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=500,
        chunk_overlap=50,
        length_function=len,
        separators=["\n\n", "\n", ". ", " ", ""]
    )

    # Split documents
    doc_chunks = text_splitter.split_documents(documents)
    print(f"Created {len(doc_chunks)} chunks")

    print("Loading embedding model...")
    embeddings = HuggingFaceInferenceAPIEmbeddings(
        model_name="intfloat/multilingual-e5-small",
        api_key=os.getenv("HUGGINGFACE_API_KEY")
    )

    # Get dimension of the embeddings
    embedding_dimension = len(embeddings.embed_query("hello"))
    print(f"Embeddings dimension: {embedding_dimension}")

    print("Creating Qdrant vector store...")
    client = QdrantClient(
        url="https://9de09ba7-f0fa-4003-9310-18b9f09eeba4.us-east4-0.gcp.cloud.qdrant.io:6333",  # Thay thế bằng URL của bạn
        api_key="ng7DyRFNkzVhiOBgE2YEnMfiBZ3pnR0p3SirSvN484HF8C8zarF6pA"  # Thay thế bằng API key của bạn
    )

    collection_name = "products_collection_384d"  # Đặt tên collection mới

    # Check if collection exists, if not then create
    collections = client.get_collections().collections
    collection_names = [collection.name for collection in collections]
    if collection_name not in collection_names:
        client.create_collection(
            collection_name=collection_name,
            vectors_config=VectorParams(
                size=embedding_dimension, distance=Distance.COSINE
            )
        )

    vector_store = Qdrant(
        client=client,
        collection_name=collection_name,
        embeddings=embeddings
    )

    # Tạo unique IDs cho từng chunk
    chunk_ids = [str(uuid4()) for _ in range(len(doc_chunks))]

    # Add documents vào vector store
    print("Adding documents to vector store...")
    vector_store.add_documents(
        documents=doc_chunks,
        ids=chunk_ids
    )

    print(f"Successfully added {len(doc_chunks)} chunks to vector store")

    # Khởi tạo các retrievers
    print("Initializing retrievers...")
    # 1. Initialize BM25 retriever
    bm25_retriever = BM25Retriever.from_documents(
        doc_chunks,
        k=3
    )

    # 2. Tạo retriever từ vector store
    vectorstore_retriever = vector_store.as_retriever(
        search_kwargs={"k": 3}
    )

    # 3. Hybrid search
    ensemble_retriever = EnsembleRetriever(
        retrievers=[vectorstore_retriever, bm25_retriever], weights=[0.3, 0.7]
    )

    # Thêm đoạn code sử dụng cross encoder ranker
    model = HuggingFaceCrossEncoder(model_name="BAAI/bge-reranker-base")
    compressor = CrossEncoderReranker(model=model, top_n=3)
    ensemble_retriever = ContextualCompressionRetriever(
        base_compressor=compressor, base_retriever=ensemble_retriever
    )

    return vector_store, ensemble_retriever

def main():
    # Tạo và lưu vector store
    vector_store, ensemble_retriever = process_and_store_documents()

    prompt = ChatPromptTemplate.from_template(RAG_SEARCH_PROMPT_TEMPLATE)

    llm = ChatGroq(temperature=0.3, model="llama-3.1-70b-versatile", api_key=os.getenv("GROQ_API_KEY"))

    # build retrieval chain using LCEL
    # this will take the user query and generate the answer
    rag_chain = (
        {"context": ensemble_retriever, "question": RunnablePassthrough()}
        | prompt
        | llm
        | StrOutputParser()
    )

    # Test tìm kiếm
    search_queries = [
        "California Roll",
        "Burger Phô Mai Truyền Thống",
        "Pepperoni Pizza",
    ]

    for query in search_queries:
        print(f"\nCâu hỏi: {query}")

        # Using similarity_search_with_score
        results_with_score = vector_store.similarity_search_with_score(query, k=3)
        for doc, score in results_with_score:
            print(f"Document: {doc.page_content}\nScore: {score}\n")

        # Using similarity_search
        results = vector_store.similarity_search(query, k=3)
        for doc in results:
            print(f"Document: {doc.page_content}\n")

        # Using similarity_search_with_relevance_scores
        results_with_relevance_scores = vector_store.similarity_search_with_relevance_scores(query)
        for doc, relevance_score in results_with_relevance_scores:
            print(f"Document: {doc.page_content}\nRelevance Score: {relevance_score}\n")

        # Using rag_chain
        result = rag_chain.invoke(query)
        print(f"Câu trả lời: {result}")

if __name__ == "__main__":
    main()