import modal
from typing import Dict

from agent import RecommendationAgent
from ingestion.ingest import (
    KnowledgeBaseIngestion
)


# ==========================================================
# Modal Image
# ==========================================================

image = (
    modal.Image.debian_slim()
    .pip_install(
        # LangChain
        "langchain",
        "langchain-core",
        "langchain-groq",
        "langchain-community",
        "langchain-text-splitters",

        # Embeddings
        "sentence-transformers",

        # Vector DB
        "qdrant-client",

        # PDF Loading
        "pypdf",

        # API
        "fastapi",
        "uvicorn",

        # Utilities
        "python-dotenv",
        "numpy"
    )
    .add_local_dir(".", remote_path="/root")
)


# ==========================================================
# Modal App
# ==========================================================

app = modal.App(
    name="Recommendation-Agent",
    image=image
)


# ==========================================================
# Recommendation Endpoint
# ==========================================================

@app.function(
    secrets=[
        modal.Secret.from_name("groq"),
        modal.Secret.from_name("DATABASE_URL"),
        modal.Secret.from_name("RAG")
    ]
)
@modal.fastapi_endpoint(
    label="recommendation",
    method="POST"
)
def recommendation(data: Dict):
    """
    Recommendation Agent Endpoint

    Input:
        Assessment JSON
        Emotion JSON
        Conversation Summary

    Output:
        recommendation_json
    """

    agent = RecommendationAgent()

    response = agent.run(data)

    return response


# ==========================================================
# Knowledge Base Ingestion
# ==========================================================

@app.function(
    timeout=3600,
    secrets=[
        modal.Secret.from_name("RAG")
    ]
)
def ingest():
    """
    Upload all knowledge base PDFs to Qdrant.
    """

    pipeline = KnowledgeBaseIngestion()

    pipeline.ingest(
        "/root/knowledge_base"
    )

    return {
        "status": "success",
        "message": "Knowledge base ingested successfully."
    }