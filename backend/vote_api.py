from flask import Blueprint, jsonify, request

from database import VALID_VOTES, get_vote_statistics, init_db, insert_vote


vote_bp = Blueprint("vote_api", __name__)

init_db()


@vote_bp.route("/vote", methods=["POST"])
def create_vote():
    data = request.get_json(silent=True) or {}
    video_id = str(data.get("video_id", "")).strip()
    vote = str(data.get("vote", "")).strip().lower()

    if not video_id:
        return jsonify({"error": "video_id is required"}), 400

    if vote not in VALID_VOTES:
        return jsonify({"error": "vote must be true, false, or unsure"}), 400

    try:
        vote_id = insert_vote(video_id, vote)
    except Exception:
        return jsonify({"error": "failed to save vote"}), 500

    return jsonify(
        {
            "message": "vote saved",
            "id": vote_id,
            "statistics": get_vote_statistics(video_id),
        }
    ), 201


@vote_bp.route("/vote/statistics")
def vote_statistics():
    video_id = request.args.get("video_id", "").strip()

    try:
        return jsonify(get_vote_statistics(video_id or None))
    except Exception:
        return jsonify({"error": "failed to load vote statistics"}), 500
