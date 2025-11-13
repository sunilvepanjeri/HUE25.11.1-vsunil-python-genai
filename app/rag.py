from app.vectorstore import VectorStore
from loguru import logger

vector_db = VectorStore()

async def chunk_and_store(text, chunk_size = 100, overlap = 50):
    documents = []
    for start in range(0, len(text), chunk_size):
        if not documents:
            documents.append(" ".join(text[start : chunk_size]))
        else:
            documents.append(" ".join(text[start - overlap : start + chunk_size]))

    logger.info("chunking complete")

  

    result = await vector_db.index_data(documents)

    return result