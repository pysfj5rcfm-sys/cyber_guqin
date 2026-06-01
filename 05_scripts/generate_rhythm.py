from pathlib import Path
import csv

ROOT = Path(__file__).resolve().parents[1]
SCORE = ROOT / "01_pieces" / "xianwengcao" / "score_events.csv"
TEMPLATES = ROOT / "00_global" / "gesture_templates.csv"
COMPONENTS = ROOT / "00_global" / "gesture_components.csv"
PHRASES = ROOT / "01_pieces" / "xianwengcao" / "phrase_structure.csv"
RHYTHM_DIR = ROOT / "01_pieces" / "xianwengcao" / "rhythm_candidates"

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

def load_components():
    result = {}
    for row in read_csv(COMPONENTS):
        result.setdefault(row["gesture_id"], []).append(row)
    return result

def validate_score_templates(score_rows, templates):
    missing = sorted({row["gesture_id"] for row in score_rows if row["gesture_id"] not in templates})
    if missing:
        raise ValueError("gesture_id missing from gesture_templates.csv: " + ", ".join(missing))

FIELDS = ["candidate_id","event_id","event_start","total_duration","pre_attack_duration","attack_time","post_motion_start","post_motion_duration","release_tail","after_gap","dynamic","reason"]
BASE = {
    "A_even": {"散音": 1.0, "按音": 1.1, "泛音": 1.0},
    "B_phrase": {"散音": 1.05, "按音": 1.35, "泛音": 1.05},
    "C_sanban": {"散音": 1.25, "按音": 1.65, "泛音": 1.20},
    "D_teaching": {"散音": 1.0, "按音": 1.15, "泛音": 1.0},
}

def main():
    score = read_csv(SCORE)
    require_score_count(score)
    templates = load_templates()
    validate_score_templates(score, templates)
    components = load_components()
    phrases = {row["phrase_id"]: row for row in read_csv(PHRASES)}
    for candidate_id, base_map in BASE.items():
        rows = []
        cursor = 0.0
        for event in score:
            template = templates[event["gesture_id"]]
            phrase = phrases[event["phrase_id"]]
            stype = template["primary_sound_type"]
            duration = base_map[stype]
            after_gap = 0.08
            post_duration = 0.0
            reasons = [f"{candidate_id} base {stype}"]
            names = {c["component_name"] for c in components[event["gesture_id"]]}
            if event["event_role"] == "phrase_end":
                duration += 0.18 if candidate_id != "C_sanban" else 0.35
                after_gap += 0.25 if candidate_id != "A_even" else 0.12
                reasons.append("phrase_end breath")
            if "shang" in names:
                post_duration = 0.75 if candidate_id != "C_sanban" else 1.25
                duration += post_duration
                reasons.append("上七九 post motion expanded")
            if "zhuang" in names:
                post_duration = 0.32
                duration += post_duration
                reasons.append("撞 micro returning slide")
            if template["gesture_family"] == "left_hand_sound" and "qiaqi" in names:
                after_gap = 0.04
                reasons.append("掐起承接前音")
            if phrase["phrase_type"] == "harmonic_closing" and stype == "泛音":
                if candidate_id in {"D_teaching", "B_phrase"}:
                    duration = 1.05
                reasons.append("泛音段更规整")
            pre = 0.12 if event["notation_pre_action"] == "zhu" else 0.0
            attack = cursor + pre
            rows.append({
                "candidate_id": candidate_id, "event_id": event["event_id"],
                "event_start": f"{cursor:.3f}", "total_duration": f"{duration:.3f}",
                "pre_attack_duration": f"{pre:.3f}", "attack_time": f"{attack:.3f}",
                "post_motion_start": f"{attack:.3f}", "post_motion_duration": f"{post_duration:.3f}",
                "release_tail": "0.300", "after_gap": f"{after_gap:.3f}",
                "dynamic": "mp", "reason": "; ".join(reasons),
            })
            cursor += duration + after_gap
        write_csv(RHYTHM_DIR / f"{candidate_id}.csv", FIELDS, rows)
        print(f"Generated {candidate_id} with {len(rows)} events.")

if __name__ == "__main__":
    main()
