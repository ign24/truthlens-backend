import os
import json
import traceback
from fastapi import APIRouter, HTTPException
from openai import OpenAI
from dotenv import load_dotenv
from backend.schemas import AnalysisRequest, AnalysisResponse

# Load environment variables from the correct path
load_dotenv(os.path.join(os.path.dirname(os.path.dirname(__file__)), '.env'))

# Initialize router
router = APIRouter()

ANALYSIS_PROMPT = """You are an expert media analyst. You will receive a short news article and must return only a JSON object with this structure:

{{
    "factual_accuracy": number between 0 and 100,
    "bias": one of ["left", "right", "neutral"],
    "emotional_tone": one of ["neutral", "alarmist", "euphoric"],
    "recommendation": string
}}

Do not include triple backticks, markdown formatting, or any explanations. Return ONLY the JSON object.

Article: {input_text}
"""

def strip_markdown_json_wrappers(text: str) -> str:
    """Remove markdown formatting from JSON response."""
    # Remove ```json or ``` from start
    text = text.strip()
    if text.startswith("```json"):
        text = text[7:]
    elif text.startswith("```"):
        text = text[3:]
    
    # Remove trailing ```
    if text.endswith("```"):
        text = text[:-3]
    
    return text.strip()

def get_openai_client():
    """Get OpenAI client with API key validation."""
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        raise HTTPException(
            status_code=500,
            detail="OpenAI API key not configured. Please set OPENAI_API_KEY in .env file."
        )
    return OpenAI(api_key=api_key)

@router.post("/analyze", response_model=AnalysisResponse)
async def analyze_text(request: AnalysisRequest) -> AnalysisResponse:
    """
    Analyze the provided text using OpenAI's GPT-4 API.
    """
    try:
        # Get OpenAI client with API key validation
        client = get_openai_client()

        # Call OpenAI API
        response = client.chat.completions.create(
            model="gpt-4o",
            messages=[
                {"role": "system", "content": "You are a JSON-only response bot. Always respond with a single, valid JSON object. No markdown, no explanations, no formatting, no additional text."},
                {"role": "user", "content": ANALYSIS_PROMPT.format(input_text=request.input_text)}
            ],
            temperature=0.1
        )

        # Get the response content
        content = response.choices[0].message.content
        print(f"Raw API response: {content}")  # Debug print

        # Clean markdown formatting
        cleaned_content = strip_markdown_json_wrappers(content)
        print(f"Cleaned content: {cleaned_content}")  # Debug print

        # Validate that the entire response is a JSON object
        try:
            analysis = json.loads(cleaned_content)
        except json.JSONDecodeError as e:
            error_msg = f"Invalid JSON response from API: {str(e)}\nFull response: {content}\nCleaned content: {cleaned_content}"
            print(error_msg)
            raise ValueError(error_msg)

        # Validate required fields
        required_fields = ["factual_accuracy", "bias", "emotional_tone", "recommendation"]
        missing_fields = [field for field in required_fields if field not in analysis]
        if missing_fields:
            raise ValueError(f"Missing required fields: {missing_fields}")

        # Validate factual_accuracy is a number between 0 and 100
        if not isinstance(analysis["factual_accuracy"], (int, float)) or not 0 <= analysis["factual_accuracy"] <= 100:
            raise ValueError("factual_accuracy must be a number between 0 and 100")

        # Validate bias is one of the allowed values
        if analysis["bias"] not in ["left", "right", "neutral"]:
            raise ValueError("bias must be one of: left, right, neutral")

        # Validate emotional_tone is one of the allowed values
        if analysis["emotional_tone"] not in ["neutral", "alarmist", "euphoric"]:
            raise ValueError("emotional_tone must be one of: neutral, alarmist, euphoric")

        # Return the validated response
        return AnalysisResponse(
            factual_accuracy=analysis["factual_accuracy"],
            bias=analysis["bias"],
            emotional_tone=analysis["emotional_tone"],
            recommendation=analysis["recommendation"]
        )

    except ValueError as e:
        print(f"Validation Error: {str(e)}")
        print(f"Traceback: {traceback.format_exc()}")
        raise HTTPException(
            status_code=500,
            detail=f"Invalid response format: {str(e)}"
        )
    except Exception as e:
        print(f"Error in analyze_text: {str(e)}")
        print(f"Traceback: {traceback.format_exc()}")
        error_detail = str(e)
        if hasattr(e, 'response'):
            try:
                error_detail = e.response.json()
            except:
                error_detail = str(e)
        raise HTTPException(
            status_code=500,
            detail=f"OpenAI API error: {error_detail}"
        ) 