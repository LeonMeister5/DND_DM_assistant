from flask import Blueprint, request, jsonify
from services.gpt4omini_monster import Gpt4oMiniMonster
# from services.volc_monster import VolcMonster

bp = Blueprint("api", __name__, url_prefix="/api")
_llm = Gpt4oMiniMonster()

# frontend need change
@bp.post("/llm_enrich")
def post_llm_enrich():
    data = request.get_json(force=True)
    theme, width, height = data.get("monster")
    if not theme or not width or not height:
        return jsonify({"error":"monster required"}), 400
    text = _llm.generate_room(theme, width, height)
    return jsonify({"description": text})
