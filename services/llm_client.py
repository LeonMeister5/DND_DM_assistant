import httpx
from config import Config

class LlmClient:
    def __init__(self, api_key: str = None, base_url: str = None, model: str = None):
        self.api_key = api_key or Config.ARK_API_KEY
        self.base_url = base_url or Config.ARK_BASE_URL
        self.model = model or Config.ARK_MODEL
        self._client = httpx.Client(base_url=self.base_url, timeout=30)

    def enrich(self, monster: dict) -> str:
        """
        调用豆包/方舟 OpenAI 兼容的 /chat/completions
        """
        headers = {"Authorization": f"Bearer {self.api_key}"}
        payload = {
            "model": self.model,
            "messages": [
                {"role":"system","content":"你是DND设定写手，生成80字以内中文描述，并给出三条战术要点。"},
                {"role":"user","content": f"怪物数据：{monster}"}
            ]
        }
        r = self._client.post("/chat/completions", headers=headers, json=payload)
        r.raise_for_status()
        data = r.json()
        return data["choices"][0]["message"]["content"]
