# AI Fluency Training

My submissions for the AI Fluency Training conducted by the Training & Placement Cell, Bannari Amman Institute of Technology.

## Structure

- **Day1** — Chatbot vs rule-based workflow vs AI agent comparison (course fee scenario)
- **Day1 Task** — Same comparison on a different scenario (library book fines), with output screenshots and a written analysis

## How to run

Each folder has its own setup:

```bash
cd Day1
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
```

Add a `.env` file with your Groq API key before running any script.

## Note

`.env` files are not pushed here — they're excluded via `.gitignore`.
