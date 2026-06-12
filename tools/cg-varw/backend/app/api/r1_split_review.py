from __future__ import annotations

from fastapi import APIRouter, HTTPException
from fastapi.responses import FileResponse

from app.schemas import (
    GenericResponse,
    R1BatchesResponse,
    R1DraftResponse,
    R1ReviewExportRequest,
    R1ReviewSaveRequest,
    R1SegmentMetadata,
    R1SegmentsResponse,
    R1WaveformResponse,
)
from app.services.r1_review_store import export_r1_csv, load_r1_draft, save_r1_draft
from app.services.r1_split_store import (
    get_split_root,
    get_split_root_mode,
    get_segment,
    list_batches,
    list_segments,
    resolve_segment_path,
    segment_metadata,
    segment_waveform,
)


router = APIRouter(prefix="/r1")


@router.get("/batches", response_model=R1BatchesResponse)
def r1_batches() -> R1BatchesResponse:
    mode = get_split_root_mode()
    message = (
        "后端已连接，当前使用合成演示 Split 根目录。"
        if mode == "demo"
        else "后端已连接，当前使用真实 Split 根目录。"
    )
    return R1BatchesResponse(
        split_root=str(get_split_root()),
        split_root_mode=mode,  # type: ignore[arg-type]
        message=message,
        batches=list_batches(),
    )


@router.get("/batches/{batch_id}/segments", response_model=R1SegmentsResponse)
def r1_batch_segments(batch_id: str) -> R1SegmentsResponse:
    response = list_segments(batch_id)
    if not response.segments:
        raise HTTPException(status_code=404, detail="R1 batch not found or empty")
    return response


@router.get("/segments/{segment_id}/metadata", response_model=R1SegmentMetadata)
def r1_segment_metadata(segment_id: str) -> R1SegmentMetadata:
    try:
        return segment_metadata(segment_id)
    except Exception as exc:
        raise HTTPException(status_code=404, detail=str(exc)) from exc


@router.get("/segments/{segment_id}/audio")
def r1_segment_audio(segment_id: str) -> FileResponse:
    try:
        path = resolve_segment_path(segment_id)
    except Exception as exc:
        raise HTTPException(status_code=404, detail=str(exc)) from exc
    if not path.exists() or not path.is_file():
        raise HTTPException(status_code=404, detail="R1 segment audio not found")
    return FileResponse(path=path, filename=path.name, media_type=_media_type(path.suffix.lower()))


@router.get("/segments/{segment_id}/waveform", response_model=R1WaveformResponse)
def r1_segment_waveform(segment_id: str, points: int = 1600) -> R1WaveformResponse:
    try:
        return segment_waveform(segment_id, points)
    except Exception as exc:
        raise HTTPException(status_code=404, detail=str(exc)) from exc


@router.get("/segments/{segment_id}/markers")
def r1_segment_markers(segment_id: str):
    try:
        segment = get_segment(segment_id)
    except Exception as exc:
        raise HTTPException(status_code=404, detail=str(exc)) from exc
    return {
        "segment_id": segment.segment_id,
        "markers": segment.markers,
        "review_only": True,
        "production_grade": False,
    }


@router.get("/reviews/{batch_id}/draft", response_model=R1DraftResponse)
def r1_review_draft(batch_id: str) -> R1DraftResponse:
    return load_r1_draft(batch_id)


@router.post("/reviews/save", response_model=GenericResponse)
def r1_save_review(request: R1ReviewSaveRequest) -> GenericResponse:
    result = save_r1_draft(request)
    return GenericResponse(path=result["path"], data={"saved": True})


@router.post("/reviews/export", response_model=GenericResponse)
def r1_export_review(request: R1ReviewExportRequest) -> GenericResponse:
    result = export_r1_csv(request)
    return GenericResponse(path=result["path"], files=result["files"], data={"contract_warnings": result.get("contract_warnings", [])})


def _media_type(suffix: str) -> str:
    return {
        ".wav": "audio/wav",
        ".wave": "audio/wav",
        ".mp3": "audio/mpeg",
        ".m4a": "audio/mp4",
        ".flac": "audio/flac",
        ".aiff": "audio/aiff",
        ".aif": "audio/aiff",
    }.get(suffix, "application/octet-stream")
