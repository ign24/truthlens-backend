from pydantic import BaseModel, Field


class AnalysisRequest(BaseModel):
    """Request model for text analysis."""
    input_text: str = Field(..., max_length=5000, description="Text to analyze (max 5000 characters)")

class AnalysisResponse(BaseModel):
    """Response model for text analysis."""
    factual_accuracy: int = Field(..., ge=0, le=100, description="Factual accuracy score (0-100)")
    bias: str = Field(..., description="Political bias (left, right, neutral)")
    emotional_tone: str = Field(..., description="Emotional tone (neutral, alarmist, euphoric)")
    recommendation: str = Field(..., description="Recommendation for the reader")