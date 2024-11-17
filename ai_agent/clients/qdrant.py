from qdrant_client import QdrantClient as Qdrant

from settings import QDRANT_API_KEY, QDRANT_URL


class QdrantClient:
    def __init__(self):
        self.client = Qdrant(url=QDRANT_URL, api_key=QDRANT_API_KEY)
