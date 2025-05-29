import streamlit as st
from PIL import Image, ImageDraw
import requests
from io import BytesIO
import base64

st.set_page_config(layout="wide")
st.title("🧩 แสดงภาพพร้อมไม้บรรทัดแบบโปรแกรมตัดต่อ")

# โหลดภาพจาก URL
url = "https://cdn.pixabay.com/photo/2024/05/26/10/15/bird-8788491_1280.jpg"
response = requests.get(url)
image = Image.open(BytesIO(response.content)).convert("RGB")

# ปรับขนาด
width = st.slider("ความกว้าง (px)", 200, 1200, 600, 50)
height = st.slider("ความสูง (px)", 200, 1000, 400, 50)
resized = image.resize((width, height))

# แปลงภาพเป็น base64
buffer = BytesIO()
resized.save(buffer, format="PNG")
img_str = base64.b64encode(buffer.getvalue()).decode()
img_uri = f"data:image/png;base64,{img_str}"

# CSS และ HTML สำหรับ ruler แบบอยู่ fixed
st.markdown("""
<style>
.ruler-top {
    position: fixed;
    top: 0;
    left: 40px;
    right: 0;
    height: 40px;
    background: #eee;
    border-bottom: 1px solid #ccc;
    z-index: 10;
    display: flex;
    font-size: 10px;
    font-family: monospace;
}
.ruler-left {
    position: fixed;
    top: 40px;
    left: 0;
    bottom: 0;
    width: 40px;
    background: #eee;
    border-right: 1px solid #ccc;
    z-index: 10;
    writing-mode: vertical-rl;
    text-orientation: mixed;
    font-size: 10px;
    font-family: monospace;
}
.scroll-area {
    margin-left: 40px;
    margin-top: 40px;
    width: 100%;
    height: 600px;
    overflow: scroll;
    position: relative;
    border: 1px solid #ccc;
    background: repeating-conic-gradient(#f8f8f8 0% 25%, white 0% 50%) 0 0 / 20px 20px;
}
</style>
""", unsafe_allow_html=True)

# วาดไม้บรรทัดบน top และ left (จำลอง)
# Top Ruler
st.markdown(f"""
<div class="ruler-top">
    {"".join(f"<div style='width:50px;text-align:center;'>{i}</div>" for i in range(0, width + 50, 50))}
</div>
<div class="ruler-left">
    {"".join(f"<div style='height:50px;text-align:center;'>{i}</div>" for i in range(0, height + 50, 50))}
</div>
""", unsafe_allow_html=True)

# แสดงภาพใน scroll area
st.markdown(f"""
<div class="scroll-area">
    <img src="{img_uri}" width="{width}" height="{height}">
</div>
""", unsafe_allow_html=True)
