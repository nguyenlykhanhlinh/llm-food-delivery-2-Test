# Env variables loader
import os
import dotenv

dotenv.load_dotenv(dotenv_path="../../.env")

# Data handlers
import pandas as pd
from sqlalchemy.orm import Session

# Utils
try:
    from data_utils import get_db, get_restaurants, get_foods
    from data_models import Restaurant, Foods
    from database import SessionLocal
except:
    from .data_utils import get_db, get_restaurants, get_foods
    from .data_models import Restaurant, Foods
    from .database import SessionLocal

# Llamaindex
from llama_index.vector_stores.qdrant import QdrantVectorStore
from llama_index.storage.storage_context import StorageContext
from llama_index import VectorStoreIndex, Document, ServiceContext
from llama_index.llms import OpenAI
from llama_index.storage.index_store import SimpleIndexStore
from llama_index.storage.docstore import SimpleDocumentStore
from llama_index import load_index_from_storage
from llama_index.retrievers import BM25Retriever, BaseRetriever
from llama_index.vector_stores.types import MetadataFilters, ExactMatchFilter
from langchain_google_genai import GoogleGenerativeAIEmbeddings

# VDBs
import qdrant_client

COLLECTION_NAME = "auto-food-order"


def create_collection(client, collection_name):
    """Creates a new collection in Qdrant if it doesn't exist"""
    try:
        client.get_collection(collection_name)
    except Exception:
        client.create_collection(
            collection_name=collection_name,
            vectors_config={"text": {"size": 768, "distance": "Cosine"}},  # For Google's text-embedding-002 model
        )


def process_restaurants():
    # Reads data from SQLite
    db = SessionLocal()
    restaurants = get_restaurants(db)
    foods = get_foods(db)

    # Processes the data for vector search
    restaurant_data = [
        {
            "id": r.id,
            "name": r.name,
            "description": r.description,
        }
        for r in restaurants
    ]

    # Initialize Qdrant client
    client = qdrant_client.QdrantClient(url=CONFIG["qdrant"]["url"], api_key=CONFIG["qdrant"]["api_key"])

    # Create collection if it doesn't exist
    create_collection(client, COLLECTION_NAME)

    # Initialize embeddings
    embeddings = GoogleGenerativeAIEmbeddings(
        model="models/text-multilingual-embedding-002", google_api_key=CONFIG["google"]["api_key"]
    )

    # Use these embeddings with Qdrant vector store
    vector_store = QdrantVectorStore(client=client, collection_name=COLLECTION_NAME, embedding_function=embeddings)

    storage_context = StorageContext.from_defaults(
        vector_store=vector_store,
    )

    llm = OpenAI(model="gpt-4")
    service_context = ServiceContext.from_defaults(chunk_size=512, llm=llm)
    nodes = service_context.node_parser.get_nodes_from_documents(documents)
    storage_context.docstore.add_documents(nodes)

    index = VectorStoreIndex.from_documents(
        documents=documents,
        storage_context=storage_context,
        service_context=service_context,
    )

    return index, nodes


def load_index():
    client = qdrant_client.QdrantClient(url=CONFIG["qdrant"]["url"], api_key=CONFIG["qdrant"]["api_key"])

    vector_store = QdrantVectorStore(
        client=client,
        collection_name=COLLECTION_NAME,
    )

    storage_context = StorageContext.from_defaults(vector_store=vector_store)
    index = VectorStoreIndex(
        [],
        storage_context=storage_context,
    )

    return index


def test_connection():
    client = qdrant_client.QdrantClient(url=CONFIG["qdrant"]["url"], api_key=CONFIG["qdrant"]["api_key"])
    try:
        # Try to list collections
        collections = client.get_collections()
        print("Successfully connected to Qdrant!")
        print(f"Available collections: {collections}")
        return True
    except Exception as e:
        print(f"Failed to connect to Qdrant: {str(e)}")
        return False


if __name__ == "__main__":
    test_connection()
