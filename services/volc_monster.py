import httpx
from config import Config

class VolcMonster:
    def __init__(self, api_key: str = None, base_url: str = None, model: str = None):
        self.api_key = api_key or Config.ARK_API_KEY
        self.base_url = base_url or Config.ARK_BASE_URL
        self.model = model or Config.ARK_MODEL
        self._client = httpx.Client(base_url=self.base_url, timeout=30)

    def build_room_prompt(self, theme: str, width: int, height: int) -> str:
        """
        生成提示词, 用于创建一个矩形房间的JSON. 
        """
        return f"""
            你是“DND 地下城房间生成器”. 

            目标: 输出一个 JSON, 描述一个矩形房间中所有的物件摆放, 只负责给出物体位置与类型. 

            生成要求: 
            1. meta 部分: 
            - theme={theme}(用户传入, 不更改)
            - room_width={width}(用户传入, 不更改)
            - room_height={height}(用户传入, 不更改)
            - entrance: {{"edge":"N|E|S|W", "pos":整数}}, 入口位置
            - exit: {{"edge":"N|E|S|W", "pos":整数}}, 出口位置, 必须在不同边, 且不在角落

            2. objects 列表: 
            - 每个元素包含: 
                - type: 类别("MONSTER_SLOT" | "陷阱" | "战利品" | "装饰")
                - detail: 文字描述(例如“裂隙陷阱”“石制宝箱”“雕像”)
                - pos: {{"x":整数, "y":整数}}, 左上角为(0, 0), 向右为x, 向下为y
                - size: {{"w":整数, "h":整数}}(仅当物件占多格时出现, 可省略)

            3. 输出必须是一个合法 JSON 对象, 不包含任何解释或额外文本. 

            输出示例: 
            {{
            "meta": {{
                "theme": "{theme}", 
                "room_width": {width}, 
                "room_height": {height}, 
                "entrance": {{"edge": "N", "pos": 3}}, 
                "exit": {{"edge": "W", "pos": 4}}
            }}, 
            "objects": [
                {{"type": "MONSTER_SLOT", "pos": {{"x": 5, "y": 3}}}}, 
                {{"type": "陷阱", "detail": "裂隙陷阱", "pos": {{"x": 3, "y": 5}}}}, 
                {{"type": "战利品", "detail": "石制宝箱", "pos": {{"x": 8, "y": 2}}}}, 
                {{"type": "装饰", "detail": "雕像", "pos": {{"x": 1, "y": 1}}}}, 
                {{"type": "装饰", "detail": "石台", "pos": {{"x": 4, "y": 4}}, "size": {{"w": 2, "h": 2}}}}
            ]
            }}
        """

    def generate_room(self, theme: str = "遗迹", width: int = 10, height: int = 8) -> str:
        """
        调用 LLM 生成一个房间JSON. 
        """
        headers = {"Authorization": f"Bearer {self.api_key}"}
        prompt = self.build_room_prompt(theme, width, height)
        payload = {
            "model": self.model, 
            "messages": [
                {"role": "system", "content": "你是DND房间生成助手, 严格输出合法JSON结构. "}, 
                {"role": "user", "content": prompt}
            ], 
            "temperature": 0.8, 
            "response_format": {"type": "json_object"}
        }

        r = self._client.post("/chat/completions", headers=headers, json=payload)
        r.raise_for_status()
        data = r.json()
        return data["choices"][0]["message"]["content"]
