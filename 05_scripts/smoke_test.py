from pathlib import Path
import subprocess
import sys

ROOT = Path(__file__).resolve().parents[1]
SCRIPTS = [
    "generate_recording_script.py",
    "make_dummy_samples.py",
    "generate_rhythm.py",
    "render_audio.py",
    "audio_viability_review.py",
]

def main():
    for script in SCRIPTS:
        path = ROOT / "05_scripts" / script
        print(f"Running {path}")
        subprocess.run([sys.executable, str(path)], cwd=ROOT, check=True)
    print("Cyber Guqin v1.0 smoke test completed.")
    print("Generated:")
    print("- recording_script.csv")
    print("- sample_assets.csv")
    print("- A/B/C/D rhythm candidates")
    print("- A/B/C/D rendered wav")
    print("- audio_viability_report")

if __name__ == "__main__":
    main()
