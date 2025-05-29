import streamlit as st
from PIL import Image
import requests
from io import BytesIO
import matplotlib.pyplot as plt

st.set_page_config(page_title="แสดงภาพนกแบบเลือกภาพ", layout="wide")
st.title("🕊️ แสดงภาพนกจาก Pixabay แบบเลือกภาพ")

# URL และชื่อภาพ
image_urls = [
    "https://cdn.pixabay.com/photo/2024/05/26/10/15/bird-8788491_1280.jpg",
    "https://cdn.pixabay.com/photo/2018/09/24/08/52/mountains-3699372_1280.jpg",
    "https://cdn.pixabay.com/photo/2019/10/14/03/26/landscape-4547734_1280.jpg"
]
image_names = ["นก 🕊️", "ภูเขา 🏔️", "ทิวทัศน์ 🌄"]

# ฟังก์ชันโหลดภาพ
def load_image(url):
    try:
        response = requests.get(url)
        response.raise_for_status()
        return Image.open(BytesIO(response.content))
    except Exception as e:
        st.error(f"โหลดภาพไม่สำเร็จ: {e}")
        return None

# ตัวแปรสถานะ
if "page" not in st.session_state:
    st.session_state.page = "gallery"
if "selected_index" not in st.session_state:
    st.session_state.selected_index = None

# แสดงหน้าแกลเลอรี่
def show_gallery():
    st.header("เลือกภาพจากแกลเลอรี่")
    cols = st.columns(3)
    for idx, url in enumerate(image_urls):
        img = load_image(url)
        if img:
            with cols[idx]:
                st.image(img, use_container_width=True, caption=image_names[idx])
                if st.button(f"เลือกภาพ: {image_names[idx]}", key=f"select_{idx}"):
                    st.session_state.selected_index = idx
                    st.session_state.page = "detail"

# แสดงหน้ารายละเอียดภาพ
def show_detail():
    st.header(f"ภาพ: {image_names[st.session_state.selected_index]}")
    image = load_image(image_urls[st.session_state.selected_index])
    if image is None:
        st.error("ไม่สามารถโหลดภาพได้")
        return

    # ปรับขนาดภาพ
    st.markdown("### ปรับขนาดภาพ")
    width = st.slider("ความกว้าง (px)", 100, 800, image.width, key="width")
    height = st.slider("ความสูง (px)", 100, 600, image.height, key="height")
    image_resized = image.resize((width, height))

    if st.button("⬅️ กลับไปหน้าแกลเลอรี่"):
        st.session_state.page = "gallery"
        return

    st.subheader("🧭 ภาพพร้อมแกน X / Y")

    # สร้าง matplotlib พร้อมแกน
    dpi = 100
    figsize = (width / dpi, height / dpi)
    fig, ax = plt.subplots(figsize=figsize)
    ax.imshow(image_resized)
    ax.set_title("Original Image", fontsize=10)
    ax.set_xlabel("X (Column)", fontsize=8)
    ax.set_ylabel("Y (Row)", fontsize=8)

    step_x = max(width // 10, 1)
    step_y = max(height // 10, 1)
    ax.grid(True, color='gray', linestyle='--', linewidth=0.4)
    ax.set_xticks(range(0, width + 1, step_x))
    ax.set_yticks(range(0, height + 1, step_y))
    ax.tick_params(axis='both', labelsize=7)

    # จัดภาพไว้ตรงกลาง
    left, center, right = st.columns([1, 3, 1])
    with center:
        st.pyplot(fig)

# รันแอป
if st.session_state.page == "gallery":
    show_gallery()
elif st.session_state.page == "detail":
    show_detail()
