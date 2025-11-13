from chromadb import PersistentClient
from settings import settings


class VectorStore:

    def __init__(self):
        self.chroma_client = PersistentClient(path='./sentence_transformer')
        self.collection = self.chroma_client.get_or_create_collection(name=settings.COLLECTION_NAME)

    async def index_data(self, insert_data):
        self.collection.upsert(
            documents=insert_data,
            ids=['id' + str(i) for i in range(len(insert_data))],
        )

        return 'successfully indexed data'

    async def query(self, query):
        if isinstance(query, str):
            query = [query]

        results = self.collection.query(
            query_texts=query,
            n_results=2
        )

        return results