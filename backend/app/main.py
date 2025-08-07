from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
import time
import logging
from .config import settings
from .api.routes import upload, search, export

logger = logging.getLogger(__name__)

app = FastAPI(title="SpecScope MVP", version="0.1.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=[o.strip() for o in settings.ALLOWED_ORIGINS.split(",")],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.middleware("http")
async def log_requests(request: Request, call_next):
    start = time.time()
    response = await call_next(request)
    duration = (time.time() - start) * 1000.0
    logger.info(f"{request.method} {request.url.path} {response.status_code} {duration:.1f}ms")
    return response

@app.get("/healthz")
async def healthz():
    return {"ok": True}

app.include_router(upload.router)
app.include_router(search.router)
app.include_router(export.router)
