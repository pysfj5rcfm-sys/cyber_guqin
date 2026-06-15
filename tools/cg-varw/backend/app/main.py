from __future__ import annotations

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.health import router as health_router
from app.api.r0_raw_files import router as r0_raw_files_router
from app.api.r0_reviews import router as r0_reviews_router
from app.api.r1_split_review import router as r1_split_review_router
from app.api.r2_phrase_review import router as r2_phrase_review_router


app = FastAPI(title="CG-VARW Backend", version="0.1.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://127.0.0.1:5173", "http://localhost:5173"],
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(health_router, prefix="/api")
app.include_router(r0_raw_files_router, prefix="/api")
app.include_router(r0_reviews_router, prefix="/api")
app.include_router(r1_split_review_router, prefix="/api")
app.include_router(r2_phrase_review_router, prefix="/api")
