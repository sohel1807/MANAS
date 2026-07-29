"""
Embedding Model

Responsible for converting text into dense vectors.
"""

from sentence_transformers import SentenceTransformer

from config import EMBEDDING_MODEL


class EmbeddingModel:
    """
    Wrapper around SentenceTransformer.

    Supports:
    - Single text embedding
    - Batch embedding
    """

    _model = None

    def __init__(self):

        if EmbeddingModel._model is None:

            print(f"Loading embedding model: {EMBEDDING_MODEL}")

            EmbeddingModel._model = SentenceTransformer(
                EMBEDDING_MODEL
            )

    def encode(self, texts, batch_size=64):
        """
        Convert text(s) into embedding vector(s).

        Parameters
        ----------
        texts : str | list[str]
            Single text or list of texts.

        batch_size : int
            Batch size for embedding generation.

        Returns
        -------
        list
            If input is a string:
                Returns a single embedding list.

            If input is a list:
                Returns a list of embedding lists.
        """

        embeddings = EmbeddingModel._model.encode(
            texts,
            batch_size=batch_size,
            normalize_embeddings=True,
            show_progress_bar=True
        )

        return embeddings.tolist()