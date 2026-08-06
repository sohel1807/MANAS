# 🧠 MANAS — Mental Wellness Assessment System

MANAS is an adaptive, AI-driven mental wellness assessment platform. It holds a conversational check-in with the user, analyzes emotions and symptoms, scores the assessment, and returns personalized, knowledge-base-backed recommendations.

**Live app:** https://manas-mental-app.streamlit.app/

## Features

- Conversational assessment via a multi-module pipeline (conversation, emotion, assessment, recommendation, memory agents)
- Emotion & symptom analysis from chat responses
- Automated scoring and report generation
- RAG-based recommendations from a curated mental health knowledge base (anxiety, depression, stress, sleep, self-esteem, etc.)
- User auth, session history, and a Streamlit dashboard

## Project Structure

```
MANAS-main/
├── frontend/                  # Streamlit UI
│   ├── app.py                 # Entry point (login/register + chat)
│   ├── pages/                 # dashboard, history, processing
│   └── components/            # sidebar, cards, charts
├── backend/
│   ├── api/                   # auth & database (FastAPI/Modal)
│   └── Agents/
│       ├── conversation_agent/    # drives the chat session
│       ├── emotion_agent/         # emotion & symptom detection
│       ├── assessment_agent/      # scoring & analysis
│       ├── memory_updater/        # updates user knowledge/memory
│       └── recommendation_agent/  # RAG recommendations + knowledge_base/ (PDFs)
├── docs/
├── requirements.txt
└── LICENSE
```

## Tech Stack

Streamlit · FastAPI · Modal · LangChain · Groq · Qdrant · Sentence-Transformers

## Getting Started

```bash
pip install -r requirements.txt
streamlit run frontend/app.py
```

The frontend talks to backend agent APIs deployed on Modal; set the relevant endpoint URLs/secrets before running locally.

## License

Licensed under the [MIT License](LICENSE).