from pathlib import Path
import csv

ROOT = Path(__file__).resolve().parents[1]
SCORE = ROOT / "01_pieces" / "xianwengcao" / "score_events.csv"
TEMPLATES = ROOT / "00_global" / "gesture_templates.csv"

def read_csv(path):
    with Path(path).open("r", encoding="utf-8", newline="") as f:
        return list(csv.DictReader(f))

def write_csv(path, fieldnames, rows):
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)

def require_score_count(rows):
    if len(rows) != 51:
        raise ValueError(f"score_events.csv must contain 51 data rows, got {len(rows)}")

def load_templates():
    return {row["gesture_id"]: row for row in read_csv(TEMPLATES)}

def validate_score_templates(score_rows, templates):
    missing = sorted({row["gesture_id"] for row in score_rows if row["gesture_id"] not in templates})
    if missing:
        raise ValueError("gesture_id missing from gesture_templates.csv: " + ", ".join(missing))

OUT = ROOT / "01_pieces" / "xianwengcao" / "recording_script.csv"
FIELDS = ["script_id","recording_id","order_no","event_id","event_range","gesture_id","normalized_name","expected_sample_type","realization_variant","realization_pre_action","realization_vibrato","recommended_pause_s","need_full_decay","notes"]
KEY_EVENTS = {"XWC_P08_N02", "XWC_P09_N01", "XWC_P09_N02", "XWC_P10_N07"}

def add_row(rows, order, event, template, sample_type, variant, pre_action, vibrato, pause, notes, event_range=""):
    rows.append({
        "script_id": f"RS_XWC_001_{order:03d}",
        "recording_id": "RS_XWC_001",
        "order_no": str(order),
        "event_id": event["event_id"],
        "event_range": event_range,
        "gesture_id": event["gesture_id"],
        "normalized_name": template["normalized_name"],
        "expected_sample_type": sample_type,
        "realization_variant": variant,
        "realization_pre_action": pre_action,
        "realization_vibrato": vibrato,
        "recommended_pause_s": f"{pause:.1f}",
        "need_full_decay": "true",
        "notes": notes,
    })

def main():
    score = read_csv(SCORE)
    require_score_count(score)
    templates = load_templates()
    validate_score_templates(score, templates)
    rows = []
    order = 1
    for event in score:
        template = templates[event["gesture_id"]]
        pause = 2.5 if event["event_id"] in KEY_EVENTS else 1.5
        family = template["gesture_family"]
        stype = template["primary_sound_type"]
        if family == "left_hand_sound":
            add_row(rows, order, event, template, "atomic", "atomic", "none", "none", pause, "掐起 atomic dummy"); order += 1
            add_row(rows, order, event, template, "context", "context", "none", "none", 3.0, "掐起 context dummy"); order += 1
            continue
        add_row(rows, order, event, template, "atomic", "straight", "none", "none", pause, "baseline straight"); order += 1
        if stype == "按音":
            if event["notation_pre_action"] == "zhu":
                add_row(rows, order, event, template, "atomic", "zhu", "zhu", "none", pause, "谱面明示注"); order += 1
            elif event["notation_pre_action"] == "chuo":
                add_row(rows, order, event, template, "atomic", "chuo", "chuo", "none", pause, "谱面明示绰"); order += 1
            else:
                add_row(rows, order, event, template, "atomic", "chuo", "chuo", "none", pause, "普通按音默认绰 realization"); order += 1
    event = next(row for row in score if row["event_id"] == "XWC_P09_N02")
    add_row(rows, order, event, templates[event["gesture_id"]], "context", "context", "none", "none", 3.0, "撞到掐起建议上下文录制", "XWC_P09_N01_to_N02")
    write_csv(OUT, FIELDS, rows)
    print(f"Generated {OUT} with {len(rows)} rows covering 51 events.")

if __name__ == "__main__":
    main()
