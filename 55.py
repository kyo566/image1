import streamlit as st
from PIL import Image
import requests
from io import BytesIO
import base64

st.title("กรอบไม้บรรทัดขนาดคงที่ ไม่ย่อ-ขยายตามรูป พร้อมรูปภาพอยู่กลางกรอบ")

# โหลดภาพ
url = "https://cdn.pixabay.com/photo/2024/05/26/10/15/bird-8788491_1280.jpg"
response = requests.get(url)
img = Image.open(BytesIO(response.content)).convert("RGB")

# กำหนดขนาดกรอบแบบคงที่
FRAME_WIDTH = 900
FRAME_HEIGHT = 600
MARGIN = 40  # สำหรับไม้บรรทัด

# ปรับขนาดรูปภาพตาม slider (แต่ไม่กระทบกรอบ)
img_width = st.slider("ความกว้างรูปภาพ (px)", 100, 1500, 1000, 50)
img_height = st.slider("ความสูงรูปภาพ (px)", 100, 1000, 700, 50)

resized = img.resize((img_width, img_height))

# แปลงภาพเป็น base64
buffer = BytesIO()
resized.save(buffer, format="PNG")
img_str = base64.b64encode(buffer.getvalue()).decode()
img_uri = f"data:image/png;base64,{img_str}"

# CSS สำหรับกรอบไม้บรรทัดและ layout
st.markdown(
    f"""
    <style>
    html, body {{
        height: 100%;
        margin: 0;
        display: flex;
        justify-content: center;
        align-items: center;
    }}
    .ruler-container {{
        position: relative;
        width: {FRAME_WIDTH + MARGIN}px;
        height: {FRAME_HEIGHT + MARGIN}px;
        border: 1px solid #ccc;
        background: #f9f9f9;
        user-select: none;
        overflow: hidden;
        margin: 0;
    }}
    .ruler-top {{
        position: absolute;
        top: 0;
        left: {MARGIN}px;
        right: 0;
        height: {MARGIN}px;
        background: #eee;
        border-bottom: 1px solid #bbb;
        display: flex;
        font-size: 11px;
        font-family: monospace;
        z-index: 10;
        overflow: hidden;
    }}
    .ruler-top div {{
        width: 50px;
        text-align: center;
        border-right: 1px solid #ccc;
        line-height: {MARGIN}px;
        white-space: nowrap;
    }}
    .ruler-left {{
        position: absolute;
        top: {MARGIN}px;
        left: 0;
        bottom: 0;
        width: {MARGIN}px;
        background: #eee;
        border-right: 1px solid #bbb;
        font-size: 11px;
        font-family: monospace;
        display: flex;
        flex-direction: column;
        align-items: center;
        justify-content: flex-start;
        padding-top: 0;
        overflow: hidden;
        user-select: none;
    }}
    .ruler-left div {{
        height: 50px;
        border-bottom: 1px solid #ccc;
        width: 40px;
        display: flex;
        align-items: center;
        justify-content: center;
        transform: rotate(-90deg);
        transform-origin: center;
        white-space: nowrap;
    }}
    .scroll-area {{
        position: absolute;
        top: {MARGIN}px;
        left: {MARGIN}px;
        width: {FRAME_WIDTH}px;
        height: {FRAME_HEIGHT}px;
        overflow: auto;

        display: flex;
        justify-content: center;
        align-items: center;

        background: repeating-conic-gradient(#f8f8f8 0% 25%, white 0% 50%) 0 0 / 20px 20px;
        border: 1px solid #ddd;
        box-sizing: content-box;
    }}
    .scroll-area img {{
        max-width: 100%;
        max-height: 100%;
        object-fit: contain;
        display: block;
    }}
    </style>

    <div class="ruler-container">
        <div class="ruler-top">
            {"".join(f"<div>{i}</div>" for i in range(0, FRAME_WIDTH + 50, 50))}
        </div>
        <div class="ruler-left">
            {"".join(f"<div>{i}</div>" for i in range(0, FRAME_HEIGHT + 50, 50))}
        </div>
        <div class="scroll-area">
            <img src="{img_uri}" width="{img_width}" height="{img_height}">
        </div>
    </div>
    """,
    unsafe_allow_html=True,
)
