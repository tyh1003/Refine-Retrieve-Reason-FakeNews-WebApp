import json
import os
import threading
from datetime import datetime


BASE_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_DIR = os.path.dirname(BASE_DIR)
DATA_DIR = os.path.join(PROJECT_DIR, "data")
VOTE_DATA_PATH = os.path.join(DATA_DIR, "votes.json")
VALID_VOTES = {"true", "false", "unsure"}

_vote_lock = threading.RLock()


def init_db():
    os.makedirs(DATA_DIR, exist_ok=True)

    if not os.path.exists(VOTE_DATA_PATH):
        write_votes([])


def read_votes():
    init_db()

    with open(VOTE_DATA_PATH, "r", encoding="utf-8") as f:
        data = json.load(f)

    if not isinstance(data, list):
        return []

    return data


def write_votes(votes):
    os.makedirs(DATA_DIR, exist_ok=True)
    temp_path = f"{VOTE_DATA_PATH}.tmp"

    with open(temp_path, "w", encoding="utf-8") as f:
        json.dump(votes, f, ensure_ascii=False, indent=2)
        f.write("\n")

    os.replace(temp_path, VOTE_DATA_PATH)


def normalize_vote_record(record):
    return {
        "video_id": str(record.get("video_id", "")).strip(),
        "user_vote": str(record.get("user_vote", "")).strip().lower(),
        "created_at": record.get("created_at"),
    }


def insert_vote(video_id, vote):
    if vote not in VALID_VOTES:
        raise ValueError("invalid vote")

    with _vote_lock:
        votes = read_votes()
        votes.append(
            {
                "video_id": video_id,
                "user_vote": vote,
                "created_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            }
        )
        write_votes(votes)

        return len(votes)


def get_vote_statistics(video_id=None):
    with _vote_lock:
        votes = [normalize_vote_record(record) for record in read_votes()]

    if video_id:
        votes = [record for record in votes if record["video_id"] == video_id]

    total = len(votes)
    true_count = sum(1 for record in votes if record["user_vote"] == "true")
    false_count = sum(1 for record in votes if record["user_vote"] == "false")
    unsure_count = sum(1 for record in votes if record["user_vote"] == "unsure")

    def percent(count):
        if total == 0:
            return 0

        return round(count * 100 / total)

    return {
        "total": total,
        "true_count": true_count,
        "false_count": false_count,
        "unsure_count": unsure_count,
        "true_percent": percent(true_count),
        "false_percent": percent(false_count),
        "unsure_percent": percent(unsure_count),
    }
