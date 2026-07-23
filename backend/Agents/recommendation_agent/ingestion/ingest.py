"""
Knowledge Base Ingestion Pipeline

Loads PDFs, splits them into chunks,
generates metadata, embeds them,
and uploads them to Qdrant.
"""

from pathlib import Path

from ingestion.pdf_loader import PDFLoader
from ingestion.chunker import DocumentChunker
from ingestion.metadata import MetadataGenerator
from ingestion.uploader import QdrantUploader


class KnowledgeBaseIngestion:
    """
    Complete knowledge base ingestion pipeline.
    """

    def __init__(self):

        self.loader = PDFLoader()

        self.chunker = DocumentChunker()

        self.metadata_generator = MetadataGenerator()

        self.uploader = QdrantUploader()

    def ingest(self, knowledge_base_path: str):
        """
        Execute the complete ingestion pipeline.

        Parameters
        ----------
        knowledge_base_path : str
            Path to the knowledge base directory.
        """

        print("=" * 60)
        print("Starting Knowledge Base Ingestion")
        print("=" * 60)

        # --------------------------------------------------
        # Step 1 : Load PDFs
        # --------------------------------------------------

        documents = self.loader.load_directory(
            knowledge_base_path
        )

        print(f"Loaded {len(documents)} pages.")

        # --------------------------------------------------
        # Step 2 : Split into chunks
        # --------------------------------------------------

        chunks = self.chunker.split(documents)

        print(f"Generated {len(chunks)} chunks.")

        # --------------------------------------------------
        # Step 3 : Generate metadata
        # --------------------------------------------------

        prepared_documents = self.metadata_generator.prepare(
            chunks
        )

        print(f"Prepared documents: {len(prepared_documents)}")

        # --------------------------------------------------
        # Step 4 : Upload to Qdrant
        # --------------------------------------------------

        self.uploader.upload(prepared_documents)

        print("=" * 60)
        print("Knowledge Base Ingestion Completed")
        print("=" * 60)


if __name__ == "__main__":

    knowledge_base = (
        Path(__file__)
        .parent.parent
        / "knowledge_base"
    )

    pipeline = KnowledgeBaseIngestion()

    pipeline.ingest(str(knowledge_base))