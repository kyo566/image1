import streamlit as st
from PIL import Image
import requests
from io import BytesIO

st.set_page_config(page_title="แสดงภาพนกจาก Pixabay", layout="wide")
st.title("🕊️ แสดงภาพนกจาก Pixabay")

# รายการ URL ของภาพ
image_urls = [
    "https://cdn.pixabay.com/photo/2024/05/26/10/15/bird-8788491_1280.jpg",
    "https://cdn.pixabay.com/photo/2016/11/22/19/45/kingfisher-1851462_1280.jpg",
    "https://cdn.pixabay.com/photo/2017/08/30/01/11/hummingbird-2695569_1280.jpg"
]

# แสดงภาพเรียงใน 3 คอลัมน์
cols = st.columns(3)

for idx, url in enumerate(image_urls):
    try:
        response = requests.get(url)
        response.raise_for_status()

        content_type = response.headers.get("Content-Type", "")
        if "image" not in content_type:
            raise ValueError(f"URL นี้ไม่ได้ส่งคืนรูปภาพ: {content_type}")

        image = Image.open(BytesIO(response.content))
        with cols[idx]:
            st.image(image, caption=f"ภาพที่ {idx+1}", use_container_width=True)

    except Exception as e:
        st.error(f"โหลดภาพที่ {idx+1} ไม่สำเร็จ: {e}")
