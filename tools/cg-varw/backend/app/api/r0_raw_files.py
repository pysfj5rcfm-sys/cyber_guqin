from __future__ import annotations

from fastapi import APIRouter, HTTPException
from fastapi.responses import FileResponse

from app.schemas import MetadataResponse, RawFilesResponse, WaveformResponse
from app.services.asr_candidate_loader import load_asr_candidates
from app.services.audio_metadata import metadata_for_file
from app.services.raw_file_scanner import scan_raw_files
from app.services.raw_root import resolve_file_id
from app.services.review_unit_builder import load_or_build_review_units
from app.services.waveform_service import waveform_for_file


router = APIRouter(prefix="/r0/raw-files")


@router.get("", response_model=RawFilesResponse)
def raw_files() -> RawFilesResponse:
    return scan_raw_files()


@router.get("/{file_id}/metadata", response_model=MetadataResponse)
def raw_file_metadata(file_id: str) -> MetadataResponse:
    path = _resolve_existing(file_id)
    return metadata_for_file(file_id, path)


@router.get("/{file_id}/audio")
def raw_file_audio(file_id: str) -> FileResponse:
    path = _resolve_existing(file_id)
    return FileResponse(path=path, filename=path.name, media_type=_media_type(path.suffix.lower()))


@router.get("/{file_id}/waveform", response_model=WaveformResponse)
def raw_file_waveform(file_id: str, points: int = 1600) -> WaveformResponse:
    path = _resolve_existing(file_id)
    return waveform_for_file(file_id, path, points)


@router.get("/{file_id}/asr-candidates")
def raw_file_asr_candidates(file_id: str):
    path = _resolve_existing(file_id)
    return load_asr_candidates(path)


@router.get("/{file_id}/review-units")
def raw_file_review_units(file_id: str):
    path = _resolve_existing(file_id)
    return load_or_build_review_units(file_id, path)


def _resolve_existing(file_id: str):
    try:
        path = resolve_file_id(file_id)
    except Exception as exc:
        raise HTTPException(status_code=404, detail=str(exc)) from exc
    if not path.exists() or not path.is_file():
        raise HTTPException(status_code=404, detail="raw file not found")
    return path


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
