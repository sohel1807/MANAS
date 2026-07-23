"""
Retriever

Responsible for:
- Converting query into embedding
- Searching Qdrant
- Returning relevant documents
"""

from embeddings import EmbeddingModel
from vector_store import VectorStore
from config import (
    TOP_K,
    SIMILARITY_THRESHOLD
)


class Retriever:

    def __init__(self):

        self.embedding_model = EmbeddingModel()

        self.vector_store = VectorStore()

    def retrieve(
        self,
        query: str,
        top_k: int = TOP_K,
        query_filter=None
    ):
        """
        Retrieve relevant knowledge from Qdrant.
        """

        # Convert query to embedding
        query_vector = self.embedding_model.encode(query)

        # Search Qdrant
        results = self.vector_store.search(
            query_vector=query_vector,
            top_k=top_k,
            query_filter=query_filter
        )

        documents = []

        for result in results:

            if result.score < SIMILARITY_THRESHOLD:
                continue

            documents.append({

                "score": result.score,

                "content": result.payload.get(
                    "content",
                    ""
                ),

                "metadata": result.payload

            })

        return documents