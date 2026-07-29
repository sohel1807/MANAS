import os
import modal

from modal import (
    App,
    Image,
    enter,
    method
)

from agent import analyze
from analysis import load_groq_model


# ==========================================================
# Modal Image
# ==========================================================

image = (
    Image.debian_slim(python_version="3.12")
    .pip_install(
        "transformers",
        "torch",
        "langchain",
        "langchain-core",
        "langchain-groq",
        "python-dotenv",
        "fastapi",
        "uvicorn[standard]"
    )
    .add_local_dir(".", remote_path="/root")
)


app = App(
    name="Memory-Agent",
    image=image
)


# ==========================================================
# Memory Service
# ==========================================================

@app.cls(
    secrets=[
        modal.Secret.from_name("groq")
    ]
)
class MemoryService:

    @enter()
    def startup(self):

        print("Loading Groq Model...")

        self.groq_model = load_groq_model(
            os.environ["GROQ_API_KEY"]
        )

        print("Groq Model Loaded")

    @method()
    def analyze(
        self,
        recent_messages,
        conversation_summary,
        covered_topics,
    ):

        return analyze(

            recent_messages=recent_messages,

            conversation_summary=conversation_summary,

            covered_topics=covered_topics,

            groq_model=self.groq_model,

        )


# ==========================================================
# FastAPI Endpoint
# ==========================================================

@app.function()
@modal.fastapi_endpoint(
    label="memory",
    method="POST"
)
def memory(info: dict):

    return MemoryService().analyze.remote(

        recent_messages=info["recent_messages"],

        conversation_summary=info.get(
            "conversation_summary",
            {
                "main_issue": "",
                "overall_summary": "",
                "current_stage": "early",
                "protective_factors": [],
                "risk_observations": []
            }
        ),

        covered_topics=info.get(
            "covered_topics",
            {
                "general": [],
                "phq9": [],
                "gad7": []
            }
        ),

    )