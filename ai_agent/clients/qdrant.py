import uuid

from qdrant_client import QdrantClient as Qdrant
from qdrant_client.http.models import PointStruct
from settings import QDRANT_API_KEY, QDRANT_URL


class QdrantClient:
    def __init__(self, collection: str = "aidevs"):
        self.client = Qdrant(url=QDRANT_URL, api_key=QDRANT_API_KEY)
        self.collection = collection

    def add_embedding(self, vector: list, metadata: dict):
        point_id = str(uuid.uuid4())
        self.client.upsert(
            collection_name=self.collection,
            points=[
                PointStruct(
                    id=point_id,
                    vector=vector,
                    payload=metadata
                )
            ]
        )


    def search_results(self, query_vector: list, limit: int = 5):
        search_results = self.client.search(
            collection_name=self.collection,
            query_vector=query_vector,
            limit=limit
        )
        return search_results