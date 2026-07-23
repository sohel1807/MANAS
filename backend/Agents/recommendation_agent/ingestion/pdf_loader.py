"""
PDF Loader

Loads all PDF documents from the knowledge base.
"""

from pathlib import Path
from langchain_community.document_loaders import PyPDFLoader


class PDFLoader:
    """
    Loads PDF documents recursively from the knowledge base.
    """

    def load_directory(self, directory: str):
        """
        Load all PDFs from a directory and its subdirectories.

        Parameters
        ----------
        directory : str

        Returns
        -------
        list
            List of LangChain Document objects.
        """

        documents = []

        pdf_files = Path(directory).rglob("*.pdf")

        for pdf_file in pdf_files:

            loader = PyPDFLoader(str(pdf_file))

            docs = loader.load()

            # Add category based on parent folder
            category = pdf_file.parent.name

            for doc in docs:
                doc.metadata["category"] = category

            documents.extend(docs)

        return documents