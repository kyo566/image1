import streamlit as st
from PIL import Image, ImageDraw, ImageFont
import requests
from io import BytesIO

st.set_page_config(page_title="แสดงภาพนกพร้อมไม้บรรทัด", layout="wide")
st.title("🖼️ แสดงภาพพร้อมปรับขนาดและไม้บรรทัด")

# รายการ URL ของภาพ
image_urls = [
    "https://cdn.pixabay.com/photo/2024/05/26/10/15/bird-8788491_1280.jpg",
    "https://cdn.pixabay.com/photo/2018/09/24/08/52/mountains-3699372_1280.jpg",
    "https://cdn.pixabay.com/photo/2019/10/14/03/26/landscape-4547734_1280.jpg"
]

# ค่าเริ่มต้นใน session_state
if "selected_index" not in st.session_state:
    st.session_state.selected_index = None
if "image_width" not in st.session_state:
    st.session_state.image_width = 400
if "image_height" not in st.session_state:
    st.session_state.image_height = 300

# แสดงภาพทั้งหมดถ้ายังไม่เลือก
if st.session_state.selected_index is None:
    cols = st.columns(3)
    for idx, url in enumerate(image_urls):
        with cols[idx]:
            try:
                response = requests.get(url)
                response.raise_for_status()
                image = Image.open(BytesIO(response.content))
                st.image(image, caption=f"ภาพที่ {idx+1}", use_container_width=True)
                if st.button(f"เลือกภาพที่ {idx+1}", key=f"btn_{idx}"):
                    st.session_state.selected_index = idx
            except Exception as e:
                st.error(f"โหลดภาพที่ {idx+1} ไม่สำเร็จ: {e}")

# แสดงภาพเดี่ยวเมื่อเลือกแล้ว
else:
    st.markdown("### 🖼️ ภาพที่คุณเลือก")
    selected_url = image_urls[st.session_state.selected_index]

    try:
        response = requests.get(selected_url)
        response.raise_for_status()
        image = Image.open(BytesIO(response.content))

        # สไลเดอร์แกน X/Y
        col1, col2 = st.columns(2)
        with col1:
            width = st.slider("ความกว้าง (แกน X)", min_value=100, max_value=1000,
                              value=st.session_state.image_width, step=50)
        with col2:
            height = st.slider("ความสูง (แกน Y)", min_value=100, max_value=1000,
                               value=st.session_state.image_height, step=50)

        st.session_state.image_width = width
        st.session_state.image_height = height

        # ปรับขนาดภาพ
        resized = image.resize((width, height))

        # วาดไม้บรรทัดบนภาพ
        ruler_img = resized.copy()
        draw = ImageDraw.Draw(ruler_img)

        # เส้นแนวแกน X (บน)
        for x in range(0, width, 50):
            draw.line([(x, 0), (x, 15)], fill="red", width=1)
            draw.text((x + 2, 16), str(x), fill="red")

        # เส้นแนวแกน Y (ซ้าย)
        for y in range(0, height, 50):
            draw.line([(0, y), (15, y)], fill="blue", width=1)
            draw.text((18, y), str(y), fill="blue")

        # แสดงภาพที่มีไม้บรรทัด
        st.image(ruler_img, caption="ภาพที่ปรับขนาดแล้ว พร้อมไม้บรรทัด")

        if st.button("🔙 กลับไปเลือกรูปอื่น"):
            st.session_state.selected_index = None

    except Exception as e:
        st.error(f"ไม่สามารถโหลดภาพที่เลือกได้: {e}")
        if st.button("🔙 กลับ"):
            st.session_state.selected_index = None
