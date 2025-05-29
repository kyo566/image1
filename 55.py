import streamlit as st
from PIL import Image
import requests
from io import BytesIO
import base64

st.title("กรอบไม้บรรทัดล้อมรูปแบบพื้นที่เฉพาะ")

# โหลดภาพ
url = "https://cdn.pixabay.com/photo/2024/05/26/10/15/bird-8788491_1280.jpg"
response = requests.get(url)
img = Image.open(BytesIO(response.content)).convert("RGB")

# ปรับขนาด
width = st.slider("ความกว้าง (px)", 200, 800, 500, 50)
height = st.slider("ความสูง (px)", 200, 600, 300, 50)
resized = img.resize((width, height))

# แปลงภาพเป็น base64
buffer = BytesIO()
resized.save(buffer, format="PNG")
img_str = base64.b64encode(buffer.getvalue()).decode()
img_uri = f"data:image/png;base64,{img_str}"

# CSS สำหรับกรอบไม้บรรทัดเฉพาะพื้นที่รูป
st.markdown(
    f"""
    <style>
    .ruler-container {{
        position: relative;
        width: {width + 40}px;  /* เพิ่มที่ว่างสำหรับไม้บรรทัด */
        height: {height + 40}px;
        border: 1px solid #ccc;
        background: #f9f9f9;
        margin: auto;
        user-select: none;
    }}
    .ruler-top {{
        position: absolute;
        top: 0;
        left: 40px;
        right: 0;
        height: 40px;
        background: #eee;
        border-bottom: 1px solid #bbb;
        display: flex;
        font-size: 11px;
        font-family: monospace;
        z-index: 10;
    }}
    .ruler-top div {{
        width: 50px;
        text-align: center;
        border-right: 1px solid #ccc;
        line-height: 40px;
    }}
    .ruler-left {{
        position: absolute;
        top: 40px;
        left: 0;
        bottom: 0;
        width: 40px;
        background: #eee;
        border-right: 1px solid #bbb;
        font-size: 11px;
        font-family: monospace;
        writing-mode: vertical-rl;
        text-orientation: mixed;
        display: flex;
        flex-direction: column;
        z-index: 10;
    }}
    .ruler-left div {{
        height: 50px;
        border-bottom: 1px solid #ccc;
        text-align: center;
        line-height: 50px;
    }}
    .scroll-area {{
        position: absolute;
        top: 40px;
        left: 40px;
        width: {width}px;
        height: {height}px;
        overflow: auto;
        background: repeating-conic-gradient(#f8f8f8 0% 25%, white 0% 50%) 0 0 / 20px 20px;
        border: 1px solid #ddd;
        box-sizing: content-box;
    }}
    </style>

    <div class="ruler-container">
        <div class="ruler-top">
            {"".join(f"<div>{i}</div>" for i in range(0, width + 50, 50))}
        </div>
        <div class="ruler-left">
            {"".join(f"<div>{i}</div>" for i in range(0, height + 50, 50))}
        </div>
        <div class="scroll-area">
            <img src="{img_uri}" width="{width}" height="{height}">
        </div>
    </div>
    """,
    unsafe_allow_html=True,
)
