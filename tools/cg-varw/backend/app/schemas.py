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
    recording_session_id: str = ""
    recording_id: str = ""
    piece_id: str = ""
    qinist_id: str = ""
    batch_id: str = ""
    recording_take_no: str = ""
    batch_take_no: str = ""
    script_id: str = ""
    source_raw_audio: str = ""
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


R1MarkerType = Literal["pre_idle_end", "gesture_start", "render_anchor", "tail_end"]
R1MarkerReviewStatus = Literal["candidate", "accepted", "unclear", "needs_retake", "rejected"]
R1AnchorType = Literal["main_attack", "gesture_start", "context_first_attach"]
R1PreAttackMusicPolicy = Literal["keep_silence", "preserve"]
R1TailPolicy = Literal["smart_fade_100ms", "full_tail"]
R1SegmentStatus = Literal["candidate", "render_usable", "reference_only", "unclear", "needs_retake", "rejected", "excluded"]
R1ReviewStatus = Literal["candidate", "not_started", "in_progress", "accepted", "unclear", "needs_retake", "rejected"]


class R1Marker(BaseModel):
    marker_id: str
    segment_id: str
    marker_type: R1MarkerType
    marker_label_zh: str
    time_s: float
    source: Literal["synthetic_candidate", "human_adjusted", "manual", "derived_from_fixture"] = "derived_from_fixture"
    confidence: float | None = None
    review_status: R1MarkerReviewStatus = "candidate"
    nudge_total_ms: int = 0
    notes: str = ""


class R1MarkerSet(BaseModel):
    pre_idle_end: R1Marker | None = None
    gesture_start: R1Marker | None = None
    render_anchor: R1Marker | None = None
    tail_end: R1Marker | None = None


class R1SegmentQC(BaseModel):
    render_usable: bool = False
    reference_only: bool = False
    unclear: bool = False
    needs_retake: bool = False
    rejected: bool = False
    reject_reason: str = ""
    noise_issue: bool = False
    click_issue: bool = False
    tail_clipped: bool = False
    attack_clipped: bool = False
    slate_residue: bool = False
    wrong_take: bool = False


class SplitBatch(BaseModel):
    batch_id: str
    display_name: str
    segment_count: int
    source: Literal["synthetic_demo", "real_split_root"]
    review_only: bool = True
    production_grade: bool = False


class SplitSegment(BaseModel):
    segment_id: str
    batch_id: str
    take_id: str
    file_name: str
    relative_path: str
    recording_session_id: str = ""
    recording_id: str = ""
    piece_id: str = ""
    qinist_id: str = ""
    recording_take_no: str = ""
    batch_take_no: str = ""
    script_id: str = ""
    source_raw_audio: str = ""
    source_split_audio: str = ""
    event_id: str = ""
    event_range: str = ""
    gesture_id: str = ""
    realization_variant: Literal["clean", "context", "retake", "demo"] | None = None
    variant: Literal["clean", "context", "retake", "demo"] = "clean"
    duration_s: float
    sample_rate: int | None = None
    bit_depth: int | None = None
    channels: int | None = None
    markers: R1MarkerSet
    anchor_type: R1AnchorType = "main_attack"
    pre_attack_music_policy: R1PreAttackMusicPolicy = "keep_silence"
    tail_policy: R1TailPolicy = "smart_fade_100ms"
    segment_status: R1SegmentStatus = "candidate"
    review_status: R1ReviewStatus = "not_started"
    qc: R1SegmentQC = Field(default_factory=R1SegmentQC)
    human_accepted: bool | None = None
    reviewed_by: str = ""
    reviewed_at: str = ""
    notes: str = ""
    synthetic_demo: bool = False
    review_only: bool = True
    production_grade: bool = False
    not_sample_assets: bool = True
    not_render_executed: bool = True
    not_ml_training_data: bool = True


class R1BatchesResponse(BaseModel):
    split_root: str
    split_root_mode: Literal["demo", "real"]
    message: str
    batches: list[SplitBatch]
    review_only: bool = True
    production_grade: bool = False


class R1SegmentsResponse(BaseModel):
    batch_id: str
    segments: list[SplitSegment]
    review_only: bool = True
    production_grade: bool = False


class R1SegmentMetadata(BaseModel):
    segment_id: str
    batch_id: str
    take_id: str
    file_name: str
    relative_path: str
    recording_session_id: str = ""
    recording_id: str = ""
    piece_id: str = ""
    qinist_id: str = ""
    recording_take_no: str = ""
    batch_take_no: str = ""
    script_id: str = ""
    source_raw_audio: str = ""
    source_split_audio: str = ""
    event_id: str = ""
    event_range: str = ""
    gesture_id: str = ""
    realization_variant: str = ""
    duration_s: float
    sample_rate: int | None = None
    bit_depth: int | None = None
    channels: int | None = None
    source_format: str
    waveform_supported: bool
    browser_playback_likely: bool
    synthetic_demo: bool = False
    review_only: bool = True
    production_grade: bool = False


class R1WaveformResponse(BaseModel):
    segment_id: str
    duration_s: float
    points: int
    peaks: list[float]
    waveform_supported: bool
    fallback_reason: str | None = None
    review_only: bool = True
    production_grade: bool = False


class R1ReviewSaveRequest(BaseModel):
    batch_id: str
    segments: list[SplitSegment]
    notes: str = ""


class R1ReviewExportRequest(R1ReviewSaveRequest):
    pass


class R1DraftResponse(BaseModel):
    batch_id: str
    exists: bool
    saved_at: str | None = None
    segments: list[SplitSegment] = Field(default_factory=list)
    review_only: bool = True
    production_grade: bool = False
