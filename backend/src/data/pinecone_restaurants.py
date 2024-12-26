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
from llama_index.settings import Settings
from llama_index.llms.openai import OpenAI

# LlamaIndex imports
from llama_index.core import (
    SimpleDirectoryReader,
    Document,
    StorageContext,
    VectorStoreIndex,
)
from llama_index.retrievers.bm25 import BM25Retriever
from llama_index.core.retrievers import BaseRetriever
from llama_index.vector_stores.pinecone import PineconeVectorStore
from llama_index.core.vector_stores import ExactMatchFilter
from llama_index.core.node_parser import SentenceSplitter

# VDBs
#import weaviate
import pinecone

ENVIRONMENT = "gcp-starter"
INDEX_NAME = "llm-food"

def process_restaurants():
    # Reading SQLite db
    db = SessionLocal()
    restaurants = get_restaurants(db)
    foods = get_foods(db)

    # Convert the data to a pandas DataFrame
    restaurant_data = [{"id": r.id, "name": r.name, "description": r.description} for r in restaurants]
    restaurant_df = pd.DataFrame(restaurant_data)

    food_data = [{"id": f.id, "restaurant_id": f.restaurant_id, "name": f.name, "description": f.description, "price": f.price} for f in foods]
    food_df = pd.DataFrame(food_data)

    # Processing for merge: renaming columns
    food_df = food_df.rename(
        columns={
            "id": "food_id",
            "restaurant_id": "id",
            "name": "food_name",
            "description": "food_description",
        }
    )

    # Merging
    df = pd.merge(restaurant_df, food_df, on="id")

    # Groupby restaurant and creating text for embedding
    df["food_text"] = "\n-" + df["food_name"] + "\n" + df["food_description"]

    df = df.groupby("id").agg({"name": "first", "description": "first", "food_text": "sum"}).reset_index()
    
    # Creating text for embedding
    df["text"] = "```" + df["name"] + "\nRestaurant description: " + df["description"] + "\nFood available:" + df["food_text"] + "\n```"

    # Llamaindex
    documents = [
        Document(
            text=df_row["text"],
            metadata={
                "search_type": "restaurant",
                "restaurant_id": df_row["id"],
                "restaurant_name": df_row["name"],
                "restaurant_description": df_row["description"],
                "restaurant_menu": df_row["food_text"],
            }
        )
        for _, df_row in df.iterrows()
    ]

    vector_store = PineconeVectorStore(
        index_name=INDEX_NAME,
        environment=ENVIRONMENT,
    )

    storage_context = StorageContext.from_defaults(
        vector_store=vector_store,
    )

    llm = OpenAI(model="gpt-3.5-turbo")

    settings = Settings(
        llm=llm,
        chunk_size=512
    )
    
    nodes = settings.node_parser.get_nodes_from_documents(documents)

    storage_context.docstore.add_documents(nodes)

    index = VectorStoreIndex.from_documents(
        documents=documents,
        storage_context=storage_context,
        settings=settings,  # Pass settings here
    )

    return index, nodes

def load_index():
    vector_store = PineconeVectorStore(
        index_name=INDEX_NAME,
        environment=ENVIRONMENT,
    )

    storage_context = StorageContext.from_defaults(vector_store=vector_store)
    
    index = VectorStoreIndex([], storage_context=storage_context)

    return index

def main():
    index, nodes = process_restaurants()

    # Hybrid retrieval
    vector_retriever = index.as_retriever(similarity_top_k=5)
    bm25_retriever = BM25Retriever.from_defaults(nodes=nodes, similarity_top_k=5)

    # Test query
    query = "I want to order sushi and ramen near my location."

    print("BM25 Results:")
    bm25_results = bm25_retriever.retrieve(query)
    for result in bm25_results:
        print(f"Restaurant: {result.node.metadata['restaurant_name']} | Score: {result.score}")

    print("\nVector Results:")
    vector_results = vector_retriever.retrieve(query)
    for result in vector_results:
        print(f"Restaurant: {result.node.metadata['restaurant_name']} | Score: {result.score}")

if __name__ == "__main__":
    main()