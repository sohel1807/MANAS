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
from emotion_model import load_emotion_model


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
    name="Emotion-NLP-Agent",
    image=image
)


@app.cls(
    secrets=[
        modal.Secret.from_name("groq")
    ]
)
class EmotionService:

    @enter()
    def startup(self):

        print("Loading Emotion Model...")

        self.emotion_model = load_emotion_model()

        print("Emotion Model Loaded")

        print("Loading Groq Model...")

        self.groq_model = load_groq_model(
            os.environ["GROQ_API_KEY"]
        )

        print("Groq Model Loaded")

    @method()
    def analyze(self, conversation):

        return analyze(
            conversation=conversation,
            emotion_model=self.emotion_model,
            groq_model=self.groq_model
    )


@app.function()
@modal.fastapi_endpoint(
    label="emotion",
    method="POST"
)
def emotion(info: dict):

    return EmotionService().analyze.remote(
        info["conversation"]
    )