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
    name="Assessment-Agent",
    image=image
)


# ==========================================================
# Assessment Service
# ==========================================================

@app.cls(
    secrets=[
        modal.Secret.from_name("groq")
    ]
)
class AssessmentService:

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
        conversation_summary,
        symptom_json,
    ):

        return analyze(

            conversation_summary=conversation_summary,

            symptom_json=symptom_json,

            groq_model=self.groq_model,

        )


# ==========================================================
# FastAPI Endpoint
# ==========================================================

@app.function()
@modal.fastapi_endpoint(
    method="POST",
    label="assessment"
)
def assessment(info: dict):

    if "conversation_summary" not in info:

        return {
            "status": "FAILED",
            "message": "conversation_summary is required."
        }

    if "symptom_json" not in info:

        return {
            "status": "FAILED",
            "message": "symptom_json is required."
        }

    return AssessmentService().analyze.remote(

        conversation_summary=info[
            "conversation_summary"
        ],

        symptom_json=info[
            "symptom_json"
        ],

    )