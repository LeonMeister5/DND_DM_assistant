from services.volc_monster import VolcMonster
import json

# 实例化模型客户端
client = VolcMonster()

# 设置测试参数
theme = "遗迹"
width = 10
height = 8

# 调用生成函数
print("正在调用 LLM 生成房间 ...")
result = client.generate_room(theme=theme, width=width, height=height)

# 输出原始返回
print("\n=== 原始返回 ===")
print(result)

# 如果是字符串形式的 JSON，尝试解析
try:
    data = json.loads(result)
    print("\n=== 解析后结构 ===")
    print(json.dumps(data, ensure_ascii=False, indent=2))
except Exception as e:
    print("\n解析失败：", e)
