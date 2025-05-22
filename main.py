from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.util import get_remote_address
from slowapi.errors import RateLimitExceeded
from slowapi.middleware import SlowAPIMiddleware
from backend.routers.analyze import router as analyze_router

limiter = Limiter(key_func=get_remote_address)

def create_app() -> FastAPI:
    app = FastAPI(
        title="TruthLens API",
        description="API for analyzing news articles and detecting bias",
        version="1.0.0"
    )

    app.state.limiter = limiter
    app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)
    app.add_middleware(SlowAPIMiddleware)

    app.add_middleware(
        CORSMiddleware,
        allow_origins=["http://localhost:5173", "https://truthlens-ai.netlify.app", "https://dulcet-pithivier-9d7373.netlify.app"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    @app.get("/")
    async def root():
        return JSONResponse({
            "message": "Welcome to TruthLens API",
            "docs": "/docs",
            "endpoints": {
                "analyze": "/api/analyze"
            }
        })

    app.include_router(analyze_router, prefix="/api", tags=["analysis"])

    return app

app = create_app()

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)