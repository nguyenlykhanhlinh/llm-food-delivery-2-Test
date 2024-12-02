from llama_index.vector_stores.qdrant import QdrantVectorStore
import qdrant_client
from llama_index.core import StorageContext
from llama_index.core import VectorStoreIndex, Document, ServiceContext


def load_qdrant_index(collection_name, CONFIG):
    """Loads the qdrant index from the collection_name"""

    client = qdrant_client.QdrantClient(url=CONFIG["qdrant"]["url"], api_key=CONFIG["qdrant"]["api_key"])

    vector_store = QdrantVectorStore(
        client=client,
        collection_name=collection_name,
    )

    storage_context = StorageContext.from_defaults(vector_store=vector_store)
    index = VectorStoreIndex([], storage_context=storage_context)

    return index


def get_retriever(collection_name: str, top_k: int, CONFIG, **kwargs):
    """Returns a retriever object from a qdrant index"""

    # Loads the index
    index = load_qdrant_index(collection_name, CONFIG)

    # Returns the retriever
    return index.as_retriever(similarity_top_k=top_k, **kwargs)
