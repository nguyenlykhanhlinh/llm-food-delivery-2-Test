import os
from dotenv import load_dotenv

load_dotenv()


class Settings:
    # Database
    DATABASE_URL = "sqlite:///./data/database.db"

    # Qdrant
    QDRANT_URL="https://9de09ba7-f0fa-4003-9310-18b9f09eeba4.us-east4-0.gcp.cloud.qdrant.io:6333"
    QDRANT_API_KEY="ng7DyRFNkzVhiOBgE2YEnMfiBZ3pnR0p3SirSvN484HF8C8zarF6pA"
    COLLECTION_NAME = "products_collection_384d"

    # HuggingFace
    HUGGINGFACE_MODEL = "intfloat/multilingual-e5-small"
    HUGGINGFACE_API_KEY = os.getenv("HUGGINGFACE_API_KEY")

    # Groq
    GROQ_MODEL = "llama-3.1-70b-versatile"
    GROQ_API_KEY = os.getenv("GROQ_API_KEY")


settings = Settings()
