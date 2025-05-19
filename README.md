# TruthLens Backend

This is the FastAPI backend for the TruthLens application, which analyzes news articles for bias and factual accuracy.

## Setup

1. Create a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

## Running the Application

To run the development server:
```bash
uvicorn main:app --reload
```

The API will be available at `http://localhost:8000`

## API Documentation

Once the server is running, you can access:
- Interactive API docs (Swagger UI): `http://localhost:8000/docs`
- Alternative API docs (ReDoc): `http://localhost:8000/redoc`

## API Endpoints

### POST /api/analyze
Analyzes a text for bias and factual accuracy.

Request body:
```json
{
    "input_text": "Your text to analyze here..."
}
```

Response:
```json
{
    "factual_accuracy": 82,
    "bias": "neutral",
    "emotional_tone": "measured",
    "recommendation": "This article appears balanced. Consider checking the sources to confirm accuracy."
}
``` 