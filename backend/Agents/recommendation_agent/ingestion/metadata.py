"""
Metadata Generator

Prepares document chunks for uploading to Qdrant.
"""

import uuid


class MetadataGenerator:
    """
    Generates metadata for document chunks.
    """

    def prepare(self, documents):
        """
        Convert LangChain Documents into dictionaries
        ready for embedding and upload.

        Parameters
        ----------
        documents : list
            List of LangChain Document objects.

        Returns
        -------
        list
            List of dictionaries.
        """

        prepared_documents = []

        for doc in documents:

            prepared_documents.append({

                "id": str(uuid.uuid4()),

                "content": doc.page_content,

                "metadata": {
                    "source": doc.metadata.get("source", ""),
                    "page": doc.metadata.get("page", 0),
                    "category": doc.metadata.get("category", "Unknown")
                }

            })

        return prepared_documents