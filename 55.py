import streamlit as st
from PIL import Image
import requests
from io import BytesIO

st.set_page_config(page_title="แสดงภาพนกจาก Pixabay", layout="wide")
st.title("🕊️ แสดงภาพนกจาก Pixabay")

# รายการ URL ของภาพ
image_urls = [
    "https://cdn.pixabay.com/photo/2024/05/26/10/15/bird-8788491_1280.jpg",
    "https://cdn.pixabay.com/photo/2020/04/14/13/48/bird-5044440_1280.jpg",
    "https://cdn.pixabay.com/photo/2017/03/07/23/54/hummingbird-2120756_1280.jpg"
]

# แสดงภาพเรียงใน 3 คอลัมน์
cols = st.columns(3)

for idx, url in enumerate(image_urls):
    try:
        response = requests.get(url)
        image = Image.open(BytesIO(response.content))
        with cols[idx]:
            st.image(image, caption=f"ภาพที่ {idx+1}", use_container_width=True)
    except Exception as e:
        st.error(f"โหลดภาพที่ {idx+1} ไม่สำเร็จ: {e}")
