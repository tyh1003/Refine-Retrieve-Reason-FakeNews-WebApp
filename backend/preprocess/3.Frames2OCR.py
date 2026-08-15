
import os
import glob
import re
import cv2
import json

from tqdm import tqdm
from Levenshtein import ratio
from paddleocr import PaddleOCR


# =========================
# Path Config
# =========================

BASE_DIR = os.path.dirname(
    os.path.abspath(__file__)
)

FRAME_ROOT = os.path.abspath(
    os.path.join(
        BASE_DIR,
        "..",
        "preprocess_output",
        "frames_16"
    )
)

OUTPUT_DIR = os.path.abspath(
    os.path.join(
        BASE_DIR,
        "..",
        "preprocess_output",
        "ocr"
    )
)

# 建立資料夾
os.makedirs(
    OUTPUT_DIR,
    exist_ok=True
)


# =========================
# PaddleOCR
# =========================

print("Loading PaddleOCR...")

ocr_model = PaddleOCR(
    use_angle_cls=True,
    lang='ch'
)

print("PaddleOCR Loaded")


# =========================
# Utils
# =========================

def load_image(image_path):

    image = cv2.imread(image_path)

    return image


def clean_text(text):

    text = re.sub(
        r'[^\u4e00-\u9fffA-Za-z0-9\s\.\,\:\%\$\#\@\-\_\/]',
        '',
        text
    )

    text = re.sub(
        r'\s+',
        ' ',
        text
    )

    return text.strip()


# =========================
# OCR Single Image
# =========================

def ocr_single_image(
    image_path,
    confidence_threshold=0.3
):

    image = load_image(image_path)

    if image is None:

        print(f"Image Load Failed: {image_path}")

        return ""

    try:

        result = ocr_model.ocr(image)

        if result is None or len(result) == 0:
            return ""

        texts = []

        for line in result[0]:

            text = line[1][0]
            score = line[1][1]

            if score < confidence_threshold:
                continue

            text = clean_text(text)

            if len(text) > 0:
                texts.append(text)

        merged_text = ' '.join(texts).strip()

        print(f"OCR: {image_path}")
        print(merged_text)
        print("=" * 50)

        return merged_text

    except Exception as e:

        print(f"OCR Error: {image_path}")

        print(e)

        return ""


# =========================
# Remove Duplicate OCR
# =========================

def remove_duplicate_texts(
    texts,
    threshold=0.7
):

    if not texts:
        return []

    unique = [texts[0]]

    for i in range(1, len(texts)):

        prev_text = unique[-1]

        current_text = texts[i]

        similarity = ratio(
            prev_text,
            current_text
        )

        if similarity < threshold:

            unique.append(current_text)

    return unique


# =========================
# OCR One Video
# =========================

def extract_text_from_frames(frame_folder):

    frame_paths = sorted(
        glob.glob(
            os.path.join(
                frame_folder,
                "frame_*.png"
            )
        )
    )

    if len(frame_paths) == 0:

        print(f"No Frames: {frame_folder}")

        return []

    texts = []

    for frame_path in frame_paths:

        text = ocr_single_image(frame_path)

        if len(text) > 1:

            texts.append(text)

    texts = remove_duplicate_texts(texts)

    return texts


# =========================
# Main
# =========================

def main():

    if not os.path.exists(FRAME_ROOT):

        print(
            f"Frame root not found: "
            f"{FRAME_ROOT}"
        )

        return

    video_folders = sorted(
        os.listdir(FRAME_ROOT)
    )

    if len(video_folders) == 0:

        print("No frame folders found")

        return

    for vid in tqdm(
        video_folders,
        desc="Processing OCR"
    ):

        frame_folder = os.path.join(
            FRAME_ROOT,
            vid
        )

        if not os.path.isdir(frame_folder):
            continue

        texts = extract_text_from_frames(
            frame_folder
        )

        ocr_text = '\n'.join(texts)

        record = {
            "vid": vid,
            "ocr": ocr_text
        }

        output_path = os.path.join(
            OUTPUT_DIR,
            f"{vid}.json"
        )

        # 覆蓋舊檔
        if os.path.exists(output_path):

            try:
                os.remove(output_path)

            except:
                pass

        with open(
            output_path,
            "w",
            encoding="utf-8"
        ) as f:

            json.dump(
                record,
                f,
                ensure_ascii=False,
                indent=2
            )

        print(f"OCR Done: {vid}")

    print("=" * 50)
    print("OCR complete")
    print("=" * 50)


# =========================
# Entry
# =========================

if __name__ == "__main__":

    main()

