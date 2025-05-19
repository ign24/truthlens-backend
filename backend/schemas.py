from pydantic import BaseModel, Field

class AnalysisRequest(BaseModel):
    """Request model for text analysis."""
    input_text: str = Field(..., description="The text to analyze")

class AnalysisResponse(BaseModel):
    """Response model for text analysis."""
    factual_accuracy: int = Field(..., ge=0, le=100, description="Factual accuracy score (0-100)")
    bias: str = Field(..., description="Political bias (left, right, neutral)")
    emotional_tone: str = Field(..., description="Emotional tone (neutral, alarmist, euphoric)")
    recommendation: str = Field(..., description="Recommendation for the reader") 