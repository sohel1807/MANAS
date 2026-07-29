"""
Document Chunker

Splits documents into smaller overlapping chunks
for better retrieval performance.
"""

from langchain_text_splitters import RecursiveCharacterTextSplitter


class DocumentChunker:
    """
    Splits LangChain documents into chunks.
    """

    def __init__(
        self,
        chunk_size: int = 500,
        chunk_overlap: int = 100
    ):

        self.text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=chunk_size,
            chunk_overlap=chunk_overlap,
            separators=[
                "\n\n",
                "\n",
                ". ",
                " ",
                ""
            ]
        )

    def split(self, documents):
        """
        Split documents into smaller chunks.

        Parameters
        ----------
        documents : list
            List of LangChain Document objects.

        Returns
        -------
        list
            List of chunked LangChain Documents.
        """

        return self.text_splitter.split_documents(documents)