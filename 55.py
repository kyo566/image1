import streamlit as st
from PIL import Image
import requests
from io import BytesIO
import matplotlib.pyplot as plt

st.set_page_config(page_title="แสดงภาพนกจาก Pixabay แบบเลือกภาพ", layout="wide")
st.title("🕊️ แสดงภาพนกจาก Pixabay แบบเลือกภาพ")

# รายการ URL ของภาพ
image_urls = [
    "https://cdn.pixabay.com/photo/2024/05/26/10/15/bird-8788491_1280.jpg",
    "https://cdn.pixabay.com/photo/2018/09/24/08/52/mountains-3699372_1280.jpg",
    "https://cdn.pixabay.com/photo/2019/10/14/03/26/landscape-4547734_1280.jpg"
]

image_names = [
    "นก 🕊️",
    "ภูเขา 🏔️",
    "ทิวทัศน์ 🌄"
]

# ฟังก์ชันโหลดภาพจาก URL
def load_image(url):
    try:
        response = requests.get(url)
        response.raise_for_status()
        return Image.open(BytesIO(response.content))
    except Exception as e:
        st.error(f"โหลดภาพไม่สำเร็จ: {e}")
        return None

# สร้าง session state ตัวเก็บหน้า (page) กับรูปที่เลือก
if "page" not in st.session_state:
    st.session_state.page = "gallery"  # หน้าแกลเลอรี่ (เลือกภาพ)
if "selected_index" not in st.session_state:
    st.session_state.selected_index = None

# หน้าแกลเลอรี่ (แสดง 3 รูป + ปุ่มเลือก)
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

# หน้าแสดงภาพรายละเอียด พร้อมปรับขนาดและไม้บรรทัด
def show_detail():
    st.header(f"ภาพ: {image_names[st.session_state.selected_index]}")
    image = load_image(image_urls[st.session_state.selected_index])
    if image is None:
        st.error("ไม่สามารถโหลดภาพได้")
        return

    # ปรับขนาดภาพ
    width = st.slider("ความกว้างของภาพ (px)", 100, 1500, image.width, key="width")
    height = st.slider("ความสูงของภาพ (px)", 100, 1000, image.height, key="height")
    image_resized = image.resize((width, height))

    # ปุ่มย้อนกลับ
    if st.button("⬅️ กลับไปหน้าแกลเลอรี่"):
        st.session_state.page = "gallery"
        return

    # แสดงภาพขยายแบบปกติ
    st.subheader("ภาพขยายแบบปกติ")
    st.image(image_resized, use_container_width=True)

    # แสดงภาพพร้อมไม้บรรทัด matplotlib
    st.subheader("ภาพพร้อมไม้บรรทัด (matplotlib)")
    fig, ax = plt.subplots(figsize=(8, 6))
    ax.imshow(image_resized)
    ax.set_title("Original Image")
    ax.set_xlabel("X (Column)")
    ax.set_ylabel("Y (Row)")

    step_x = max(width // 10, 1)
    step_y = max(height // 10, 1)
    ax.grid(True, color='gray', linestyle='--', linewidth=0.5)
    ax.set_xticks(range(0, width+1, step_x))
    ax.set_yticks(range(0, height+1, step_y))

    st.pyplot(fig)

# เลือกแสดงหน้าตามสถานะ
if st.session_state.page == "gallery":
    show_gallery()
elif st.session_state.page == "detail":
    show_detail()
