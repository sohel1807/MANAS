"""
Configuration for Recommendation Agent

Reads configuration values from Modal Secrets.
"""

import os

# ==========================================================
# Qdrant Configuration
# ==========================================================

QDRANT_URL = os.getenv("QDRANT_URL")
QDRANT_API_KEY = os.getenv("QDRANT_KEY")

QDRANT_COLLECTION = os.getenv(
    "QDRANT_COLLECTION",
    "manas_knowledge"
)

# ==========================================================
# Embedding Configuration
# ==========================================================

EMBEDDING_MODEL = os.getenv(
    "EMBEDDING_MODEL",
    "BAAI/bge-base-en-v1.5"
)

EMBEDDING_DIMENSION = int(
    os.getenv("EMBEDDING_DIMENSION", "768")
)

# ==========================================================
# Retrieval Configuration
# ==========================================================

TOP_K = int(
    os.getenv("TOP_K", "5")
)

SIMILARITY_THRESHOLD = float(
    os.getenv("SIMILARITY_THRESHOLD", "0.65")
)

# ==========================================================
# Configuration Validation
# ==========================================================

def validate_config():
    """
    Validate required environment variables.
    """

    required = {
        "QDRANT_URL": QDRANT_URL,
        "QDRANT_API_KEY": QDRANT_API_KEY,
    }

    missing = [key for key, value in required.items() if not value]

    if missing:
        raise ValueError(
            f"Missing required environment variables: {', '.join(missing)}"
        )


# Validate configuration on import
# validate_config()