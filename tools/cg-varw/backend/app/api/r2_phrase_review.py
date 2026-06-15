from __future__ import annotations

from typing import Any

from fastapi import APIRouter, HTTPException

from app.schemas import GenericResponse, R2DraftPayload, R2ExportRequest
from app.services import r2_mock_store as store


router = APIRouter(prefix="/r2")


@router.get("/projects")
def r2_projects() -> dict[str, Any]:
    return {"projects": store.list_projects(), **store.SAFETY}


@router.get("/projects/{project_id}/sessions")
def r2_project_sessions(project_id: str) -> dict[str, Any]:
    if project_id != "CG_VARW":
        raise HTTPException(status_code=404, detail="R2 mock project not found")
    return {"project_id": project_id, "sessions": store.list_sessions(), **store.SAFETY}


@router.get("/sessions/{recording_session_id}/pieces")
def r2_session_pieces(recording_session_id: str) -> dict[str, Any]:
    if recording_session_id not in {session.recording_session_id for session in store.list_sessions()}:
        raise HTTPException(status_code=404, detail="R2 mock session not found")
    return {"recording_session_id": recording_session_id, "pieces": store.list_pieces(), **store.SAFETY}


@router.get("/render-sets")
def r2_render_sets() -> dict[str, Any]:
    return {"render_sets": store.list_render_sets(), **store.SAFETY}


@router.get("/render-sets/{render_set_id}")
def r2_render_set(render_set_id: str):
    return _handle(lambda: store.get_render_set(render_set_id))


@router.get("/render-sets/{render_set_id}/versions")
def r2_versions(render_set_id: str) -> dict[str, Any]:
    return _handle(lambda: {"versions": store.list_versions(render_set_id), **store.SAFETY})


@router.get("/render-sets/{render_set_id}/phrases")
def r2_phrases(render_set_id: str) -> dict[str, Any]:
    return _handle(lambda: store.list_phrases(render_set_id))


@router.get("/render-sets/{render_set_id}/phrase-alignments")
def r2_phrase_alignments(render_set_id: str) -> dict[str, Any]:
    return _handle(lambda: {"phrase_alignments": store.list_alignments(render_set_id), **store.SAFETY})


@router.get("/render-sets/{render_set_id}/event-timeline")
def r2_event_timeline(render_set_id: str) -> dict[str, Any]:
    return _handle(lambda: store.event_timeline(render_set_id))


@router.get("/render-sets/{render_set_id}/reviews/draft")
def r2_review_draft(render_set_id: str):
    return _handle(lambda: store.load_draft(render_set_id))


@router.get("/render-sets/{render_set_id}/exports")
def r2_exports(render_set_id: str) -> dict[str, Any]:
    return _handle(lambda: {"exports": store.export_rows(render_set_id), **store.SAFETY})


@router.get("/render-sets/{render_set_id}/versions/{version_id}/waveform")
def r2_waveform(render_set_id: str, version_id: str, points: int = 1600) -> dict[str, Any]:
    _handle(lambda: store.get_render_set(render_set_id))
    return {"render_set_id": render_set_id, "version_id": version_id, "points": points, "peaks": store.mock_waveform(points), "mock_render": True, **store.SAFETY}


@router.get("/render-sets/{render_set_id}/versions/{version_id}/spectrogram")
def r2_spectrogram(render_set_id: str, version_id: str, points: int = 800) -> dict[str, Any]:
    _handle(lambda: store.get_render_set(render_set_id))
    return {"render_set_id": render_set_id, "version_id": version_id, "points": points, "bins": store.mock_spectrogram(points), "mock_render": True, **store.SAFETY}


@router.get("/render-sets/{render_set_id}/versions/{version_id}/audio")
def r2_audio_mock(render_set_id: str, version_id: str) -> dict[str, Any]:
    _handle(lambda: store.get_render_set(render_set_id))
    return {"render_set_id": render_set_id, "version_id": version_id, "audio_path": f"mock://r2/{version_id}", "message": "R2A mock only; no real audio endpoint.", "mock_render": True, **store.SAFETY}


@router.post("/phrase-structure/save", response_model=GenericResponse)
def r2_phrase_structure_save(payload: dict[str, Any]) -> GenericResponse:
    result = _handle(lambda: store.save_payload("phrase_structure", payload))
    return GenericResponse(path=result["path"], data={"saved": True, **store.SAFETY})


@router.post("/phrase-alignment/save", response_model=GenericResponse)
def r2_phrase_alignment_save(payload: dict[str, Any]) -> GenericResponse:
    result = _handle(lambda: store.save_payload("phrase_alignment", payload))
    return GenericResponse(path=result["path"], data={"saved": True, **store.SAFETY})


@router.post("/listening-review/save", response_model=GenericResponse)
def r2_listening_review_save(payload: dict[str, Any]) -> GenericResponse:
    result = _handle(lambda: store.save_payload("listening_review", payload))
    return GenericResponse(path=result["path"], data={"saved": True, **store.SAFETY})


@router.post("/render-revision/save", response_model=GenericResponse)
def r2_render_revision_save(payload: dict[str, Any]) -> GenericResponse:
    result = _handle(lambda: store.save_payload("render_revision", payload))
    return GenericResponse(path=result["path"], data={"saved": True, **store.SAFETY})


@router.post("/preferred-version/save", response_model=GenericResponse)
def r2_preferred_version_save(payload: dict[str, Any]) -> GenericResponse:
    result = _handle(lambda: store.save_payload("preferred_version", payload))
    return GenericResponse(path=result["path"], data={"saved": True, **store.SAFETY})


@router.post("/reviews/draft/save", response_model=GenericResponse)
def r2_draft_save(payload: R2DraftPayload) -> GenericResponse:
    result = _handle(lambda: store.save_draft(payload))
    return GenericResponse(path=result["path"], data={"saved": True, **store.SAFETY})


@router.post("/reviews/{render_set_id}/export", response_model=GenericResponse)
def r2_export(render_set_id: str, payload: R2ExportRequest | None = None) -> GenericResponse:
    request = payload or R2ExportRequest(render_set_id=render_set_id)
    if request.render_set_id != render_set_id:
        raise HTTPException(status_code=400, detail="render_set_id path/body mismatch")
    result = _handle(lambda: store.export_reviews(request))
    return GenericResponse(path=result["path"], files=result["files"], data=store.SAFETY)


@router.get("/reviews/{render_set_id}/exports/{export_id}")
def r2_export_detail(render_set_id: str, export_id: str) -> dict[str, Any]:
    _handle(lambda: store.get_render_set(render_set_id))
    return {"render_set_id": render_set_id, "export_id": export_id, "message": "Mock export detail placeholder; files are review-only artifacts.", **store.SAFETY}


def _handle(fn):
    try:
        return fn()
    except ValueError as exc:
        raise HTTPException(status_code=404, detail=str(exc)) from exc
