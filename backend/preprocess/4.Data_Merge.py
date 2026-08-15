import os
import json
import glob
import shutil


# =========================
# Config
# =========================

ROOT_DIR = "preprocess_output"

OCR_DIR = os.path.join(
    ROOT_DIR,
    "ocr"
)

TRANSCRIPT_DIR = os.path.join(
    ROOT_DIR,
    "transcript"
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

    transcript_files = glob.glob(
        os.path.join(
            TRANSCRIPT_DIR,
            "*.json"
        )
    )

    if len(transcript_files) == 0:

        print("No transcript files")

        return

    results = []

    for transcript_path in transcript_files:

        transcript_data = load_json(
            transcript_path
        )

        vid = transcript_data.get(
            "vid",
            ""
        )

        transcript = transcript_data.get(
            "transcript",
            ""
        )

        ocr_path = os.path.join(
            OCR_DIR,
            f"{vid}.json"
        )

        ocr_data = load_json(
            ocr_path
        )

        ocr = ocr_data.get(
            "ocr",
            ""
        )

        record = {
            "vid": vid,
            "transcript": transcript,
            "ocr": ocr
        }

        results.append(record)

    # =========================
    # 只保留最新一筆
    # =========================

    latest = results[-1]

    # =========================
    # 每次覆蓋 all.json
    # =========================

    with open(
        OUTPUT_FILE,
        "w",
        encoding="utf-8"
    ) as f:

        json.dump(
            latest,
            f,
            ensure_ascii=False,
            indent=2
        )

    print("=" * 50)

    print("Data Merge Done")

    print(f"Saved: {OUTPUT_FILE}")

    print("=" * 50)


# =========================

if __name__ == "__main__":

    main()