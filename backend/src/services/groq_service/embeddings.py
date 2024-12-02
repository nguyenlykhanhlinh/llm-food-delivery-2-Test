from tenacity import retry, wait_random, stop_after_attempt
from langchain_google_genai import GoogleGenerativeAIEmbeddings


@retry(wait=wait_random(min=1, max=5), stop=stop_after_attempt(5))
async def embeddings(content, CONFIG, client=None):
    """Receives content in text and embeds it using Google's model"""

    embeddings_model = GoogleGenerativeAIEmbeddings(
        model="models/text-multilingual-embedding-002", google_api_key=CONFIG["google"]["api_key"]
    )

    # Get embeddings for the content
    response = await embeddings_model.embed_query(content)

    return response
