from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from backend.routers.analyze import router as analyze_router

def create_app() -> FastAPI:
    app = FastAPI(
        title="TruthLens API",
        description="API for analyzing news articles and detecting bias",
        version="1.0.0"
    )

    # Configure CORS
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["http://localhost:5173"],  # Frontend URL
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    # Root endpoint
    @app.get("/")
    async def root():
        return JSONResponse({
            "message": "Welcome to TruthLens API",
            "docs": "/docs",
            "endpoints": {
                "analyze": "/api/analyze"
            }
        })

    # Include routers
    app.include_router(analyze_router, prefix="/api", tags=["analysis"])

    return app

app = create_app()

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True) 