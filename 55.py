import streamlit as st
from PIL import Image
import requests
from io import BytesIO
import base64

st.title("กรอบไม้บรรทัดคงที่ เลขไม้บรรทัดเลื่อนตาม Scroll รูป")

# โหลดภาพ
url = "https://cdn.pixabay.com/photo/2024/05/26/10/15/bird-8788491_1280.jpg"
response = requests.get(url)
img = Image.open(BytesIO(response.content)).convert("RGB")

# ขนาดกรอบไม้บรรทัดคงที่
FRAME_WIDTH = 900
FRAME_HEIGHT = 600
MARGIN = 40

# ปรับขนาดรูปภาพ
img_width = st.slider("ความกว้างรูปภาพ (px)", 100, 1500, 1000, 50)
img_height = st.slider("ความสูงรูปภาพ (px)", 100, 1000, 700, 50)
resized = img.resize((img_width, img_height))

# แปลงรูปเป็น base64
buffer = BytesIO()
resized.save(buffer, format="PNG")
img_str = base64.b64encode(buffer.getvalue()).decode()
img_uri = f"data:image/png;base64,{img_str}"

# สร้าง HTML + CSS + JS
html_code = f"""
<style>
html, body {{
    height: 100%;
    margin: 0;
    display: flex;
    justify-content: center;
    align-items: center;
    background: #f0f0f0;
}}

.ruler-container {{
    position: relative;
    width: {FRAME_WIDTH + MARGIN}px;
    height: {FRAME_HEIGHT + MARGIN}px;
    border: 1px solid #aaa;
    background: #fff;
    user-select: none;
    box-shadow: 0 0 10px rgba(0,0,0,0.1);
}}

.ruler-top {{
    position: absolute;
    top: 0;
    left: {MARGIN}px;
    right: 0;
    height: {MARGIN}px;
    background: #eee;
    border-bottom: 1px solid #bbb;
    font-family: monospace;
    font-size: 11px;
    overflow: hidden;
    white-space: nowrap;
}}

.ruler-top div {{
    display: inline-block;
    width: 50px;
    text-align: center;
    border-right: 1px solid #ccc;
    line-height: {MARGIN}px;
}}

.ruler-left {{
    position: absolute;
    top: {MARGIN}px;
    left: 0;
    bottom: 0;
    width: {MARGIN}px;
    background: #eee;
    border-right: 1px solid #bbb;
    font-family: monospace;
    font-size: 11px;
    overflow: hidden;
}}

.ruler-left div {{
    height: 50px;
    border-bottom: 1px solid #ccc;
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
    background: repeating-conic-gradient(#f8f8f8 0% 25%, white 0% 50%) 0 0 / 20px 20px;
    border: 1px solid #ddd;
    box-sizing: content-box;
    display: flex;
    justify-content: center;
    align-items: center;
}}

.scroll-area img {{
    max-width: none;  /* ไม่จำกัด */
    max-height: none;
    display: block;
}}

</style>

<div class="ruler-container">
    <div class="ruler-top" id="ruler-top">
        {"".join(f"<div>{i}</div>" for i in range(0, FRAME_WIDTH + 50, 50))}
    </div>
    <div class="ruler-left" id="ruler-left">
        {"".join(f"<div>{i}</div>" for i in range(0, FRAME_HEIGHT + 50, 50))}
    </div>
    <div class="scroll-area" id="scroll-area">
        <img src="{img_uri}" width="{img_width}" height="{img_height}">
    </div>
</div>

<script>
const scrollArea = document.getElementById('scroll-area');
const rulerTop = document.getElementById('ruler-top');
const rulerLeft = document.getElementById('ruler-left');

scrollArea.addEventListener('scroll', () => {{
    // เลื่อนเลขไม้บรรทัดตาม scroll
    rulerTop.style.transform = `translateX(${-scrollArea.scrollLeft}px)`;
    rulerLeft.style.transform = `translateY(${-scrollArea.scrollTop}px)`;
}});
</script>
"""

st.components.v1.html(html_code, height=FRAME_HEIGHT + MARGIN + 20, scrolling=False)
