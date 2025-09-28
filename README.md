# DND_DM_assistant
An AI powered DND monster random generation tool. 

# How to use
python -m venv .venv
source .venv/bin/activate   # Windows 用 .venv\Scripts\activate
pip install -r requirements.txt
cp .env.example .env        # 填好 ARK_API_KEY / ARK_MODEL
python app.py
# 浏览器打开 http://127.0.0.1:5000
