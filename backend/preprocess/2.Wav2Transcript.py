import os
import sys
import torch
import json
import shutil

from transformers import (
    AutoModelForSpeechSeq2Seq,
    AutoProcessor,
    pipeline
)

# =========================
# Whisper 設定
# =========================

device = "cuda:0" if torch.cuda.is_available() else "cpu"

torch_dtype = (
    torch.float16
    if torch.cuda.is_available()
    else torch.float32
)

model_id = "openai/whisper-tiny"

print("Loading Whisper model...")

model = AutoModelForSpeechSeq2Seq.from_pretrained(
    model_id,
    torch_dtype=torch_dtype,
    low_cpu_mem_usage=True
).to(device)

processor = AutoProcessor.from_pretrained(model_id)

pipe = pipeline(
    "automatic-speech-recognition",
    model=model,
    tokenizer=processor.tokenizer,
    feature_extractor=processor.feature_extractor,
    chunk_length_s=30,
    batch_size=4,
    torch_dtype=torch_dtype,
    device=device,
)

print("Whisper loaded")


# =========================
# 單檔轉文字
# =========================

def transcribe_audio(audio_path):

    result = pipe(audio_path)

    return result["text"]


# =========================
# Main
# =========================

if __name__ == "__main__":

    video_path = sys.argv[1]

    video_name = os.path.splitext(
        os.path.basename(video_path)
    )[0]

    audio_path = os.path.join(
        "preprocess_output",
        "audio",
        f"{video_name}.wav"
    )

    output_folder = os.path.join(
        "preprocess_output",
        "transcript"
    )

    os.makedirs(
        output_folder,
        exist_ok=True
    )

    output_path = os.path.join(
        output_folder,
        f"{video_name}.json"
    )
    
    print("開始語音轉文字...")
    print("Audio:", audio_path)

    text = transcribe_audio(audio_path)

    # =========================
    # Save JSON
    # =========================

    record = {
        "vid": video_name,
        "transcript": text
    }

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

    print("Transcript Done")
    print("Output:", output_path)