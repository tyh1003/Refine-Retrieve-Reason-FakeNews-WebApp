import os
import glob
import shutil
import logging
import sys

import cv2
import numpy as np

from skimage.metrics import structural_similarity as ssim


logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

MAX_FRAMES = 16

SSIM_THRESHOLD = 0.99


# =========================
# Utils
# =========================

def load_image_gray(image_path):

    image = cv2.imread(image_path)

    if image is None:
        return None

    gray = cv2.cvtColor(
        image,
        cv2.COLOR_BGR2GRAY
    )

    return gray


def compute_ssim(img1_path, img2_path):

    img1 = load_image_gray(img1_path)

    img2 = load_image_gray(img2_path)

    if img1 is None or img2 is None:
        return 0

    if img1.shape != img2.shape:

        img2 = cv2.resize(
            img2,
            (img1.shape[1], img1.shape[0])
        )

    score = ssim(img1, img2)

    return score


# =========================
# SSIM Filtering
# =========================

def remove_high_ssim_frames(frame_paths):

    if len(frame_paths) <= 2:
        return frame_paths

    selected = [frame_paths[0]]

    prev_frame = frame_paths[0]

    for current_frame in frame_paths[1:-1]:

        score = compute_ssim(
            prev_frame,
            current_frame
        )

        if score < SSIM_THRESHOLD:

            selected.append(current_frame)

            prev_frame = current_frame

    if frame_paths[-1] != selected[-1]:

        selected.append(frame_paths[-1])

    return selected


# =========================
# Uniform Sampling
# =========================

def uniform_sample_frames(frame_paths):

    if len(frame_paths) <= MAX_FRAMES:
        return frame_paths

    indices = np.linspace(
        0,
        len(frame_paths) - 1,
        MAX_FRAMES,
        dtype=int
    )

    sampled = [
        frame_paths[idx]
        for idx in indices
    ]

    return sampled


# =========================
# Save
# =========================

def save_frames(sampled_frames, output_folder):

    # 每次重跑前清空
    if os.path.exists(output_folder):

        shutil.rmtree(output_folder)

    os.makedirs(
        output_folder,
        exist_ok=True
    )

    for idx, frame_path in enumerate(sampled_frames):

        output_path = os.path.join(
            output_folder,
            f"frame_{idx + 1}.png"
        )

        shutil.copy(
            frame_path,
            output_path
        )


# =========================
# Main
# =========================

def process_video_folder(folder_path):

    video_name = os.path.basename(folder_path)

    frame_paths = sorted(
        glob.glob(
            os.path.join(folder_path, "frame_*.png")
        )
    )

    if len(frame_paths) == 0:

        logging.warning(
            f"No frames: {folder_path}"
        )

        return

    original_count = len(frame_paths)

    # Step 1
    filtered_frames = remove_high_ssim_frames(
        frame_paths
    )

    # Step 2
    sampled_frames = uniform_sample_frames(
        filtered_frames
    )

    # Step 3
    output_folder = os.path.join(
        "preprocess_output/frames_16",
        video_name
    )

    save_frames(
        sampled_frames,
        output_folder
    )

    logging.info(
        f"{video_name} | "
        f"{original_count} -> "
        f"{len(filtered_frames)} -> "
        f"{len(sampled_frames)}"
    )

    print("Frames Compress Done")


# =========================
# Entry
# =========================

if __name__ == "__main__":

    video_path = sys.argv[1]

    video_name = os.path.splitext(
        os.path.basename(video_path)
    )[0]

    frame_folder = os.path.join(
        "preprocess_output/frames",
        video_name
    )

    process_video_folder(frame_folder)