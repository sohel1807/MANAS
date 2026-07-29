"""
Qdrant Uploader

Embeds document chunks and uploads them to Qdrant.
"""

from qdrant_client.models import PointStruct

from embeddings import EmbeddingModel
from vector_store import VectorStore


class QdrantUploader:
    """
    Uploads prepared documents into Qdrant.
    """

    def __init__(self):

        self.embedding_model = EmbeddingModel()

        self.vector_store = VectorStore()

    def upload(self, documents):
        """
        Embed documents and upload them to Qdrant.

        Parameters
        ----------
        documents : list
            Output from MetadataGenerator.prepare().
        """

        print("=" * 60)
        print("Starting embedding generation...")
        print("=" * 60)

        if not documents:
            print("No documents received.")
            return

        # --------------------------------------------------
        # Extract text from all documents
        # --------------------------------------------------

        texts = [doc["content"] for doc in documents]

        print(f"Documents received: {len(texts)}")
        print("Generating embeddings...")

        # --------------------------------------------------
        # Batch embedding generation
        # --------------------------------------------------

        vectors = self.embedding_model.encode(
            texts,
            batch_size=64
        )

        print(f"Generated {len(vectors)} embeddings.")

        # --------------------------------------------------
        # Build Qdrant points
        # --------------------------------------------------

        points = []

        for document, vector in zip(documents, vectors):

            payload = {
                "content": document["content"],
                **document["metadata"]
            }

            point = PointStruct(
                id=document["id"],
                vector=vector,
                payload=payload
            )

            points.append(point)

        print(f"Points created: {len(points)}")

        # --------------------------------------------------
        # Create collection
        # --------------------------------------------------

        self.vector_store.create_collection()

        # --------------------------------------------------
        # Upload
        # --------------------------------------------------

        print("Uploading to Qdrant...")

        batch_size = 250

        total_batches = (len(points) + batch_size - 1) // batch_size

        for i in range(0, len(points), batch_size):

            batch = points[i:i + batch_size]

            batch_number = (i // batch_size) + 1

            print(
                f"Uploading batch {batch_number}/{total_batches} "
                f"({len(batch)} points)"
            )

            self.vector_store.upload_documents(batch)

            print(
                f"✓ Batch {batch_number}/{total_batches} uploaded successfully."
            )

        print("=" * 60)
        print(f"Successfully uploaded {len(points)} chunks.")
        print("=" * 60)