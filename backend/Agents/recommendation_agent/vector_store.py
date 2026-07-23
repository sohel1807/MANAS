"""
Qdrant Vector Store

Responsible for:
- Connecting to Qdrant
- Creating collections
- Uploading document vectors
- Searching vectors
"""

from qdrant_client import QdrantClient
from qdrant_client.models import (
    Distance,
    VectorParams,
    PointStruct,
    Filter,
)

from config import (
    QDRANT_URL,
    QDRANT_API_KEY,
    QDRANT_COLLECTION,
    EMBEDDING_DIMENSION,
)


class VectorStore:
    """
    Wrapper around Qdrant Client.
    """

    def __init__(self):
        """
        Initialize Qdrant client.
        """

        self.client = QdrantClient(
            url=QDRANT_URL,
            api_key=QDRANT_API_KEY
        )

    # ==========================================================
    # Collection
    # ==========================================================

    def create_collection(self):
        """
        Create collection if it does not exist.
        """

        collections = self.client.get_collections()

        collection_names = [
            collection.name
            for collection in collections.collections
        ]

        if QDRANT_COLLECTION in collection_names:
            print(f"Collection '{QDRANT_COLLECTION}' already exists.")
            return

        self.client.create_collection(
            collection_name=QDRANT_COLLECTION,
            vectors_config=VectorParams(
                size=EMBEDDING_DIMENSION,
                distance=Distance.COSINE
            )
        )

        print(f"Collection '{QDRANT_COLLECTION}' created successfully.")

    # ==========================================================
    # Upload Documents
    # ==========================================================

    def upload_documents(self, points):
        """
        Upload document chunks to Qdrant.

        Parameters
        ----------
        points : List[PointStruct]
        """

        self.client.upsert(
            collection_name=QDRANT_COLLECTION,
            points=points
        )

    # ==========================================================
    # Search
    # ==========================================================

    def search(
    self,
    query_vector,
    top_k=5,
    query_filter=None
    ):
        """
        Search similar vectors.
        """

        response = self.client.query_points(
            collection_name=QDRANT_COLLECTION,
            query=query_vector,
            limit=top_k,
            query_filter=query_filter,
        )

        return response.points

    # ==========================================================
    # Delete Collection
    # ==========================================================

    def delete_collection(self):
        """
        Delete collection.
        """

        self.client.delete_collection(
            collection_name=QDRANT_COLLECTION
        )

    # ==========================================================
    # Collection Exists
    # ==========================================================

    def collection_exists(self):
        """
        Check whether collection exists.
        """

        collections = self.client.get_collections()

        names = [
            collection.name
            for collection in collections.collections
        ]

        return QDRANT_COLLECTION in names

    # ==========================================================
    # Collection Info
    # ==========================================================

    def get_collection_info(self):
        """
        Get collection information.
        """

        return self.client.get_collection(
            collection_name=QDRANT_COLLECTION
        )