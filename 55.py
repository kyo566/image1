import streamlit as st
from PIL import Image
import requests
from io import BytesIO

# ตั้งชื่อหน้าเว็บ
st.set_page_config(page_title="แสดงภาพจาก URL", layout="centered")

st.title("แสดงภาพจาก URL")

# URL ของรูปภาพ
image_url = "https://cdn.pixabay.com/photo/2024/05/26/10/15/bird-8788491_1280.jpg"

# ดึงรูปภาพจาก URL
try:
    response = requests.get(image_url)
    image = Image.open(BytesIO(response.content))

    # แสดงรูปภาพ
    st.image(image, caption="นกสวยงามจาก Pixabay", use_column_width=True)

except Exception as e:
    st.error(f"ไม่สามารถโหลดภาพได้: {e}")
