import json, random, pathlib
DATA_PATH = pathlib.Path(__file__).resolve().parents[1] / "data" / "monsters.json"

def load_monsters():
    with open(DATA_PATH, "r", encoding="utf-8") as f:
        return json.load(f)

_MONSTERS = load_monsters()

def random_monster(constraints=None):
    pool = _MONSTERS
    if constraints:
        for c in constraints:
            pool = [m for m in pool if c in m.get("tags", []) or c == m.get("env")]
    return random.choice(pool) if pool else random.choice(_MONSTERS)
