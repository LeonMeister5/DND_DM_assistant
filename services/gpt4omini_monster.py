import httpx
import os
import json
from dotenv import load_dotenv

load_dotenv()

class Gpt4oMiniMonster:
    """
    DND 房间生成客户端
    使用 OpenAI GPT-4o-mini 模型。
    """

    def __init__(self, api_key: str = None, base_url: str = None, model: str = None):
        self.api_key = api_key or os.getenv("OPENAI_API_KEY", "")
        self.base_url = base_url or os.getenv("OPENAI_BASE_URL", "https://api.openai.com/v1")
        self.model = model or os.getenv("OPENAI_MODEL", "gpt-4o-mini")
        self._client = httpx.Client(base_url=self.base_url, timeout=60.0)

    def build_room_prompt(self, theme: str, width: int, height: int) -> str:
        """
        构造提示词，生成矩形房间的 JSON。
        """
        return f"""
            你是“DND 地下城房间生成器”。

            目标: 输出一个 JSON, 描述一个矩形房间中所有的物件摆放, 只负责给出物体位置与类型。

            生成要求:
            1. meta 部分:
            - theme={theme}
            - room_width={width}
            - room_height={height}
            - entrance: {{"edge":"N|E|S|W","pos":整数}} 入口位置
            - exit: {{"edge":"N|E|S|W","pos":整数}} 出口位置, 不在角落且不同边

            2. objects 列表:
            - 每个元素包含:
                - type: 类别 ("MONSTER_SLOT" | "陷阱" | "战利品" | "装饰")
                - detail: 文字描述 (例如 "裂隙陷阱", "石制宝箱", "雕像")
                - pos: {{"x":整数,"y":整数}} 左上角为(0,0), 向右为x, 向下为y
                - size: {{"w":整数,"h":整数}} (仅当占多格时出现)

            3. 严格输出合法 JSON, 不包含任何解释或额外文本。
        """

    def generate_room(self, theme: str = "遗迹", width: int = 10, height: int = 8) -> str:
        """
        调用 OpenAI GPT-4o-mini 生成房间 JSON。
        """
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json",
        }

        prompt = self.build_room_prompt(theme, width, height)
        payload = {
            "model": self.model,
            "messages": [
                {"role": "system", "content": "你是DND房间生成助手, 严格输出合法JSON结构。"},
                {"role": "user", "content": prompt},
            ],
            "temperature": 0.8,
            "response_format": {"type": "json_object"},
        }

        resp = self._client.post("/chat/completions", headers=headers, json=payload)
        resp.raise_for_status()
        data = resp.json()
        return data["choices"][0]["message"]["content"]
