from __future__ import annotations

from dataclasses import dataclass, field

from app.schemas import ReviewUnit, SplitSegment


@dataclass(frozen=True)
class ExportContext:
    values: dict[str, str]
    warnings: list[str] = field(default_factory=list)


class R0ExportContextResolver:
    required_fields = (
        "recording_session_id",
        "recording_id",
        "piece_id",
        "qinist_id",
        "batch_id",
        "recording_take_no",
        "batch_take_no",
        "script_id",
        "source_raw_audio",
    )

    def resolve(self, *, file_id: str, source_audio: str, unit: ReviewUnit) -> ExportContext:
        values = {
            "recording_session_id": unit.recording_session_id,
            "recording_id": unit.recording_id,
            "piece_id": unit.piece_id,
            "qinist_id": unit.qinist_id,
            "batch_id": unit.batch_id,
            "recording_take_no": unit.recording_take_no,
            "batch_take_no": unit.batch_take_no,
            "script_id": unit.script_id,
            "source_raw_audio": unit.source_raw_audio or source_audio,
            "take_id": unit.takeId,
            "source_audio": unit.source_raw_audio or source_audio,
            "file_id": file_id,
            "event_id": unit.event_id,
            "event_range": unit.event_range,
            "gesture_id": unit.gesture_id,
            "expected_sample_type": unit.expected_sample_type,
        }
        warnings = _missing_warnings("R0", unit.id, values, self.required_fields)
        if unit.takeId and not unit.recording_take_no:
            warnings.append(f"R0 {unit.id}: recording_take_no missing; take_id retained only as display alias")
        return ExportContext(values=values, warnings=warnings)


class R1ExportContextResolver:
    required_fields = (
        "recording_session_id",
        "recording_id",
        "piece_id",
        "qinist_id",
        "batch_id",
        "recording_take_no",
        "batch_take_no",
        "script_id",
        "source_split_audio",
        "event_id",
        "event_range",
        "gesture_id",
        "realization_variant",
    )

    def resolve(self, segment: SplitSegment) -> ExportContext:
        realization_variant = segment.realization_variant or segment.variant
        source_split_audio = segment.source_split_audio or segment.relative_path
        values = {
            "recording_session_id": segment.recording_session_id,
            "recording_id": segment.recording_id,
            "piece_id": segment.piece_id,
            "qinist_id": segment.qinist_id,
            "batch_id": segment.batch_id,
            "recording_take_no": segment.recording_take_no,
            "batch_take_no": segment.batch_take_no,
            "script_id": segment.script_id,
            "take_id": segment.take_id,
            "segment_id": segment.segment_id,
            "source_raw_audio": segment.source_raw_audio,
            "source_split_audio": source_split_audio,
            "source_audio": source_split_audio,
            "event_id": segment.event_id,
            "event_range": segment.event_range,
            "gesture_id": segment.gesture_id,
            "realization_variant": realization_variant,
            "variant": realization_variant,
        }
        warnings = _missing_warnings("R1", segment.segment_id, values, self.required_fields)
        if segment.take_id and not segment.recording_take_no:
            warnings.append(f"R1 {segment.segment_id}: recording_take_no missing; take_id retained only as display alias")
        return ExportContext(values=values, warnings=warnings)


def _missing_warnings(stage: str, row_id: str, values: dict[str, str], required_fields: tuple[str, ...]) -> list[str]:
    return [f"{stage} {row_id}: missing upstream provenance for {field}" for field in required_fields if not values.get(field)]
