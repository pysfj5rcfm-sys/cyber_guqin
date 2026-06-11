from __future__ import annotations

from typing import Any, Literal

from pydantic import BaseModel, Field


class Marker(BaseModel):
    id: str | None = None
    unitId: str | None = None
    key: str
    label: str = ""
    time: float
    color: str = "cyan"
    optional: bool | None = None
    weak: bool | None = None
    displayLabel: bool | None = None
    source: str = "manual"
    confidence: float | None = None
    review_status: str = "candidate"
    nudge_total_ms: int = 0
    notes: str = ""


class ReviewUnit(BaseModel):
    id: str
    sequence: int
    unit_status: str = "needs_review"
    review_status: str = "not_started"
    source: str = "manual"
    takeId: str = ""
    boundary_type: Literal["next_slate_start", "file_end"] | None = None
    boundary_unlinked: bool = False
    notes: str = ""
    recording_take_no: str = ""
    batch_take_no: str = ""
    event_id: str = ""
    event_range: str = ""
    gesture_id: str = ""
    expected_sample_type: str = ""
    markers: list[Marker] = Field(default_factory=list)


class SaveReviewRequest(BaseModel):
    file_id: str
    units: list[ReviewUnit]
    source_audio: str | None = None
    notes: str = ""


class ExportReviewRequest(SaveReviewRequest):
    pass


class RawFileItem(BaseModel):
    file_id: str
    name: str
    relative_path: str
    size_bytes: int
    modified_time: str
    source_format: str
    review_only: bool = True
    production_grade: bool = False


class RawFilesResponse(BaseModel):
    raw_root: str
    raw_root_mode: Literal["demo", "real"]
    files: list[RawFileItem]
    review_only: bool = True
    production_grade: bool = False


class HealthResponse(BaseModel):
    ok: bool = True
    service: str = "cg-varw-backend"
    review_only: bool = True
    production_grade: bool = False


class MetadataResponse(BaseModel):
    file_id: str
    source_audio: str
    duration_s: float | None
    sample_rate: int | None
    bit_depth: int | None
    channels: int | None
    source_format: str
    size_bytes: int
    modified_time: str
    waveform_supported: bool
    browser_playback_likely: bool
    warning: str | None = None
    review_only: bool = True
    production_grade: bool = False


class WaveformResponse(BaseModel):
    file_id: str
    waveform_supported: bool
    points: int
    peaks: list[float]
    warning: str | None = None
    review_only: bool = True
    production_grade: bool = False


class GenericResponse(BaseModel):
    ok: bool = True
    path: str | None = None
    files: list[str] = Field(default_factory=list)
    data: dict[str, Any] = Field(default_factory=dict)
    review_only: bool = True
    production_grade: bool = False
