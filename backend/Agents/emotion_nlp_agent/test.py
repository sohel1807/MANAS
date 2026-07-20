import os
from dotenv import load_dotenv


from agent import EmotionNLPAgent
load_dotenv()

api_key = os.getenv("GROQ_API_KEY")
if __name__ == "__main__":

    conversation = [

        {

            "role":"user",

            "content":"I'm feeling stressed because of work."

        },

        {

            "role":"assistant",

            "content":"I'm sorry to hear that."

        },

        {

            "role":"user",

            "content":"I'm not sleeping properly."

        }

    ]

    agent = EmotionNLPAgent(
        api_key=api_key
    )

    result = agent.analyze(
        conversation
    )

    print(result)