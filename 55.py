import streamlit as st
from PIL import Image
import requests
from io import BytesIO
import matplotlib.pyplot as plt

st.set_page_config(page_title="แสดงภาพนกจาก Pixabay พร้อมแกนไม้บรรทัด", layout="wide")
st.title("🕊️ เลือกรูปภาพนกจาก Pixabay พร้อมปรับขนาดและไม้บรรทัด")

# รายการ URL ของภาพ
image_urls = [
    "https://cdn.pixabay.com/photo/2024/05/26/10/15/bird-8788491_1280.jpg",
    "https://cdn.pixabay.com/photo/2018/09/24/08/52/mountains-3699372_1280.jpg",
    "https://cdn.pixabay.com/photo/2019/10/14/03/26/landscape-4547734_1280.jpg"
]

# ชื่อภาพสำหรับ dropdown
image_names = [
    "นก 🕊️",
    "ภูเขา 🏔️",
    "ทิวทัศน์ 🌄"
]

# เลือกรูปภาพ
selected_index = st.selectbox("เลือกภาพ", options=range(len(image_urls)), format_func=lambda x: image_names[x])

# โหลดภาพ
try:
    response = requests.get(image_urls[selected_index])
    response.raise_for_status()
    image = Image.open(BytesIO(response.content))
except Exception as e:
    st.error(f"โหลดภาพไม่สำเร็จ: {e}")
    st.stop()

# ปรับขนาดภาพ
width = st.slider("ความกว้างของภาพ (px)", 100, 1500, image.width)
height = st.slider("ความสูงของภาพ (px)", 100, 1000, image.height)
image_resized = image.resize((width, height))

# แสดงภาพขยาย (แบบปกติ)
st.subheader("ภาพขยาย")
st.image(image_resized, use_container_width=True)

# แสดงภาพพร้อมแกนไม้บรรทัด (matplotlib)
st.subheader("ภาพพร้อมไม้บรรทัด (matplotlib)")

fig, ax = plt.subplots(figsize=(8, 6))
ax.imshow(image_resized)
ax.set_title("Original Image")
ax.set_xlabel("X (Column)")
ax.set_ylabel("Y (Row)")

# เปิดกริดไม้บรรทัด และกำหนด ticks ตามขนาดภาพ
step_x = max(width // 10, 1)
step_y = max(height // 10, 1)
ax.grid(True, color='gray', linestyle='--', linewidth=0.5)
ax.set_xticks(range(0, width+1, step_x))
ax.set_yticks(range(0, height+1, step_y))

st.pyplot(fig)
