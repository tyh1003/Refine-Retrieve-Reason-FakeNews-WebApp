import os
import sys
import subprocess
import glob
import shutil
import logging

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)


def get_video_duration(video_path):

    try:

        result = subprocess.run(
            [
                'ffprobe',
                '-v', 'error',
                '-show_entries', 'format=duration',
                '-of', 'default=noprint_wrappers=1:nokey=1',
                video_path
            ],
            capture_output=True,
            text=True,
            check=True
        )

        return float(result.stdout.strip())

    except Exception as e:

        logging.error(
            f"ffprobe failed: {video_path} | {e}"
        )

        return None


def generate_timestamps(duration):

    timestamps = []

    current = 0

    while current < int(duration):

        timestamps.append(float(current))

        current += 1

    if duration not in timestamps:

        timestamps.append(duration)

    return timestamps


def extract_frames_every_second(
    video_path,
    output_folder
):

    duration = get_video_duration(video_path)

    if duration is None or duration <= 0:

        logging.error(
            f"Invalid video: {video_path}"
        )

        return

    video_name = os.path.splitext(
        os.path.basename(video_path)
    )[0]

    video_output_folder = os.path.join(
        output_folder,
        video_name
    )

    # =========================
    # 每次重跑前清空舊資料
    # =========================

    if os.path.exists(video_output_folder):

        shutil.rmtree(video_output_folder)

    os.makedirs(
        video_output_folder,
        exist_ok=True
    )

    # =========================

    timestamps = generate_timestamps(duration)

    for idx, ts in enumerate(timestamps):

        output_file = os.path.join(
            video_output_folder,
            f"frame_{idx:04d}.png"
        )

        output_file = os.path.abspath(output_file)

        try:

            subprocess.run(
                [
                    'ffmpeg',

                    '-y',

                    '-ss', str(ts),

                    '-i', video_path,

                    '-frames:v', '1',

                    output_file
                ],
                check=True
            )

        except subprocess.CalledProcessError:

            logging.warning(
                f"{video_name}: failed at {ts}"
            )

    extracted = glob.glob(
        os.path.join(
            video_output_folder,
            "frame_*.png"
        )
    )

    logging.info(
        f"{video_name}: extracted {len(extracted)} frames"
    )


if __name__ == "__main__":

    if len(sys.argv) < 2:

        print("請輸入影片路徑")

        sys.exit(1)

    video_path = sys.argv[1]

    BASE_DIR = os.path.dirname(
        os.path.abspath(__file__)
    )

    output_folder = os.path.join(
        BASE_DIR,
        "..",
        "preprocess_output",
        "frames"
    )

    output_folder = os.path.abspath(
        output_folder
    )

    os.makedirs(
        output_folder,
        exist_ok=True
    )

    extract_frames_every_second(
        video_path,
        output_folder
    )

    print("Extract Frames Done")