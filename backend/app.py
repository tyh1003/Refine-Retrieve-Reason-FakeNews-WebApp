import json
import os
from concurrent.futures import ThreadPoolExecutor

from flask import Flask, jsonify, request
from flask_cors import CORS
from werkzeug.utils import secure_filename

from pipeline import run_pipeline
from status_store import process_status, reset_status, update_status
from vote_api import vote_bp


BASE_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_DIR = os.path.dirname(BASE_DIR)
UPLOAD_FOLDER = os.path.join(BASE_DIR, "uploads")
OUTPUT_DIR = os.path.join(BASE_DIR, "output")
ANSWER_PATH = os.path.join(PROJECT_DIR, "answer.jsonl")
ANSWER_NOT_FOUND_TEXT = "找不到對應答案"

app = Flask(__name__)
CORS(app)
app.register_blueprint(vote_bp)

os.makedirs(UPLOAD_FOLDER, exist_ok=True)

executor = ThreadPoolExecutor(max_workers=1)
answer_index = None


def read_latest_jsonl(path):
    if not os.path.exists(path):
        raise FileNotFoundError(path)

    with open(path, "r", encoding="utf-8") as f:
        lines = [line.strip() for line in f if line.strip()]

    if not lines:
        raise ValueError("empty jsonl")

    return json.loads(lines[-1])


def read_json_file(path):
    if not os.path.exists(path):
        raise FileNotFoundError(path)

    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


def normalize_video_id(value):
    filename = os.path.basename(str(value or "").strip())
    stem, _extension = os.path.splitext(filename)

    return stem or filename


def data_matches_current_video(data):
    current_filename = process_status.get("filename")

    if not current_filename:
        return False

    return normalize_video_id(data.get("vid")) == normalize_video_id(current_filename)


def load_answer_index():
    global answer_index

    if answer_index is not None:
        return answer_index

    index = {}

    if not os.path.exists(ANSWER_PATH):
        answer_index = index
        return answer_index

    with open(ANSWER_PATH, "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue

            try:
                item = json.loads(line)
            except json.JSONDecodeError:
                continue

            vid = str(item.get("vid", "")).strip()
            if vid:
                index[vid] = item.get("label")

    answer_index = index
    return answer_index


def get_correct_answer_fields(filename):
    label = load_answer_index().get(normalize_video_id(filename))

    try:
        normalized_label = int(label)
    except (TypeError, ValueError):
        normalized_label = None

    if normalized_label == 0:
        return {
            "correct_answer": "真",
            "correct_answer_vote": "true",
            "correct_answer_label": 0,
        }

    if normalized_label == 1:
        return {
            "correct_answer": "假",
            "correct_answer_vote": "false",
            "correct_answer_label": 1,
        }

    return {
        "correct_answer": ANSWER_NOT_FOUND_TEXT,
        "correct_answer_vote": None,
        "correct_answer_label": None,
    }


def normalize_ai_vote(data):
    raw_value = data.get("ai_vote", data.get("pred_label", data.get("label")))

    if isinstance(raw_value, bool):
        return "true" if raw_value else "false"

    if isinstance(raw_value, int):
        if raw_value == 0:
            return "true"
        if raw_value == 1:
            return "false"
        return "unsure"

    value = str(raw_value).strip().lower()
    if value in {"true", "real", "genuine", "0", "真"}:
        return "true"
    if value in {"false", "fake", "1", "假"}:
        return "false"
    if value in {"unsure", "unknown", "uncertain", "不確定"}:
        return "unsure"

    return "unsure"


def add_student_compat_fields(data):
    result = dict(data)
    result["ai_vote"] = normalize_ai_vote(result)

    if "confidence" not in result:
        result["confidence"] = result.get("conf")

    if "conf" not in result:
        result["conf"] = result.get("confidence")

    return result


@app.route("/")
def home():
    return {"message": "backend ok"}


@app.route("/status")
def get_status():
    status = dict(process_status)
    status.update(get_correct_answer_fields(status.get("filename")))

    return jsonify(status)


@app.route("/upload", methods=["POST"])
def upload_video():
    if "video" not in request.files:
        return {"error": "video is required"}, 400

    file = request.files["video"]
    filename = secure_filename(file.filename or "")

    if not filename:
        return {"error": "filename is required"}, 400

    save_path = os.path.join(UPLOAD_FOLDER, filename)
    file.save(save_path)

    run_id = reset_status(filename=filename)
    update_status("影片已上傳，準備分析...", "尚未開始", "uploaded", run_id=run_id)
    executor.submit(run_pipeline, save_path, run_id)

    response = {
        "message": "upload success",
        "filename": filename,
        "run_id": run_id,
    }
    response.update(get_correct_answer_fields(filename))

    return response


@app.route("/result")
def get_result():
    retrieve_path = os.path.join(OUTPUT_DIR, "retrieve.jsonl")

    try:
        data = read_latest_jsonl(retrieve_path)
        if not data_matches_current_video(data):
            return {"error": "retrieve result not found"}, 404

        return jsonify(data)
    except FileNotFoundError:
        return {"error": "retrieve result not found"}, 404
    except ValueError:
        return {"error": "empty retrieve result"}, 404
    except json.JSONDecodeError:
        return {"error": "invalid retrieve result"}, 500


@app.route("/student_result")
def get_student_result():
    candidate_paths = [
        os.path.join(OUTPUT_DIR, "student_result.json"),
        os.path.join(OUTPUT_DIR, "final_result.json"),
    ]

    for path in candidate_paths:
        try:
            data = read_json_file(path)
            if not data_matches_current_video(data):
                continue

            return jsonify(add_student_compat_fields(data))
        except FileNotFoundError:
            continue
        except json.JSONDecodeError:
            return {"error": "invalid student result"}, 500

    return {"error": "no student result"}, 404


if __name__ == "__main__":
    app.run(
        debug=True,
        use_reloader=False,
    )
