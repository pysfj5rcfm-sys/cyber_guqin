from __future__ import annotations

from fastapi import APIRouter

from app.schemas import ExportReviewRequest, GenericResponse, SaveReviewRequest
from app.services.marker_store import save_review_draft
from app.services.r0_export_writer import export_review_csv


router = APIRouter(prefix="/r0/reviews")


@router.post("/save", response_model=GenericResponse)
def save_review(request: SaveReviewRequest) -> GenericResponse:
    result = save_review_draft(request)
    return GenericResponse(path=result["path"], data={"saved": True})


@router.post("/export", response_model=GenericResponse)
def export_review(request: ExportReviewRequest) -> GenericResponse:
    result = export_review_csv(request)
    return GenericResponse(path=result["path"], files=result["files"], data={"contract_warnings": result.get("contract_warnings", [])})
