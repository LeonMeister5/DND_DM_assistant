from flask import Blueprint, request, jsonify
from services.rand_service import random_monster
from services.llm_client import LlmClient

bp = Blueprint("api", __name__, url_prefix="/api")
_llm = LlmClient()

@bp.get("/random_monster")
def get_random_monster():
    cons = request.args.get("constraints", "")
    constraints = [c.strip() for c in cons.split(",") if c.strip()]
    m = random_monster(constraints)
    return jsonify(m)

@bp.post("/llm_enrich")
def post_llm_enrich():
    data = request.get_json(force=True)
    m = data.get("monster")
    if not m:
        return jsonify({"error":"monster required"}), 400
    text = _llm.enrich(m)
    return jsonify({"description": text})
