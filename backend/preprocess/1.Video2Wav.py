import subprocess
from pathlib import Path
import sys


def convert_one(video_path, output_folder):

    video_path = Path(video_path)

    output_folder = Path(output_folder)

    output_folder.mkdir(
        parents=True,
        exist_ok=True
    )

    output_path = output_folder / f"{video_path.stem}.wav"


    # =========================

    cmd = [
        'ffmpeg',

        '-y',

        '-i', str(video_path),

        # 不輸出影像
        '-vn',

        # mono
        '-ac', '1',

        # 16kHz
        '-ar', '16000',

        # wav codec
        '-acodec', 'pcm_s16le',

        '-threads', '1',

        '-loglevel', 'error',

        str(output_path)
    ]

    try:

        subprocess.run(
            cmd,
            check=True
        )

        print("Audio Extract Done")
        print(output_path)

    except subprocess.CalledProcessError:

        print("Audio Extract Failed")


if __name__ == "__main__":

    video_path = sys.argv[1]

    output_folder = "preprocess_output/audio"

    convert_one(
        video_path,
        output_folder
    )