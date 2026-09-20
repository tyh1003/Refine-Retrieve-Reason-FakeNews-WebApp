import os
import json
import sys


# =========================
# Config
# =========================

ROOT_DIR = "preprocess_output"

TRANSCRIPT_DIR = os.path.join(
    ROOT_DIR,
    "transcript"
)

VLM_DIR = os.path.join(
    ROOT_DIR,
    "vlm"
)

OUTPUT_FILE = os.path.join(
    ROOT_DIR,
    "all.json"
)


# =========================
# Utils
# =========================

def load_json(path):

    if not os.path.exists(path):
        return {}

    with open(
        path,
        "r",
        encoding="utf-8"
    ) as f:

        return json.load(f)


# =========================
# Main
# =========================

def main():

    if len(sys.argv) < 2:
        print("Missing video path")
        sys.exit(1)

    video_path = sys.argv[1]

    vid = os.path.splitext(
        os.path.basename(video_path)
    )[0]


    # =========================
    # Transcript
    # =========================

    transcript_path = os.path.join(
        TRANSCRIPT_DIR,
        f"{vid}.json"
    )

    transcript_data = load_json(
        transcript_path
    )

    transcript = transcript_data.get(
        "transcript",
        ""
    )


    # =========================
    # VLM
    # =========================

    vlm_path = os.path.join(
        VLM_DIR,
        f"{vid}.json"
    )

    vlm_data = load_json(
        vlm_path
    )

    description = vlm_data.get(
        "description",
        ""
    )


    # =========================
    # Merge
    # =========================

    record = {
        "vid": vid,
        "transcript": transcript,
        "description": description
    }


    # =========================
    # 覆蓋 all.json
    # =========================

    with open(
        OUTPUT_FILE,
        "w",
        encoding="utf-8"
    ) as f:

        json.dump(
            record,
            f,
            ensure_ascii=False,
            indent=2
        )


    print("=" * 50)
    print("Data Merge Done")
    print(f"VID: {vid}")
    print(f"Transcript: {transcript_path}")
    print(f"VLM: {vlm_path}")
    print(f"Saved: {OUTPUT_FILE}")
    print("=" * 50)


# =========================

if __name__ == "__main__":
    main()