import streamlit as st
from PIL import Image, ImageDraw, ImageFont
import requests
from io import BytesIO

st.set_page_config(page_title="แสดงภาพพร้อมกรอบไม้บรรทัด", layout="wide")
st.title("🖼️ แสดงภาพพร้อมปรับขนาดและกรอบไม้บรรทัด")

# รายการภาพ
image_urls = [
    "https://cdn.pixabay.com/photo/2024/05/26/10/15/bird-8788491_1280.jpg",
    "https://cdn.pixabay.com/photo/2018/09/24/08/52/mountains-3699372_1280.jpg",
    "https://cdn.pixabay.com/photo/2019/10/14/03/26/landscape-4547734_1280.jpg"
]

# Session State
if "selected_index" not in st.session_state:
    st.session_state.selected_index = None
if "image_width" not in st.session_state:
    st.session_state.image_width = 400
if "image_height" not in st.session_state:
    st.session_state.image_height = 300

# ฟังก์ชันวาดไม้บรรทัดแบบกรอบ
def draw_ruler_frame(image, step=50, margin=40):
    width, height = image.size
    new_width = width + margin
    new_height = height + margin

    # สร้างพื้นหลังสีเทาอ่อน
    bg = Image.new("RGB", (new_width, new_height), color="#f0f0f0")
    bg.paste(image, (margin, margin))

    draw = ImageDraw.Draw(bg)

    # ไม้บรรทัดด้านบน (แกน X)
    for x in range(0, width, step):
        pos = x + margin
        draw.line([(pos, margin - 15), (pos, margin)], fill="black", width=1)
        draw.text((pos + 2, 2), str(x), fill="black")

    # ไม้บรรทัดด้านซ้าย (แกน Y)
    for y in range(0, height, step):
        pos = y + margin
        draw.line([(margin - 15, pos), (margin, pos)], fill="black", width=1)
        draw.text((2, pos - 7), str(y), fill="black")

    return bg

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

# แสดงภาพเดี่ยวพร้อมกรอบไม้บรรทัด
else:
    st.markdown("### ✂️ ปรับขนาดพร้อมกรอบไม้บรรทัด")
    selected_url = image_urls[st.session_state.selected_index]

    try:
        response = requests.get(selected_url)
        response.raise_for_status()
        image = Image.open(BytesIO(response.content))

        # สไลเดอร์ขนาด
        col1, col2 = st.columns(2)
        with col1:
            width = st.slider("ความกว้าง (แกน X)", 100, 1000, st.session_state.image_width, 50)
        with col2:
            height = st.slider("ความสูง (แกน Y)", 100, 1000, st.session_state.image_height, 50)

        st.session_state.image_width = width
        st.session_state.image_height = height

        resized = image.resize((width, height))
        final_img = draw_ruler_frame(resized, step=50, margin=40)

        st.image(final_img, caption="ภาพพร้อมกรอบไม้บรรทัด", use_column_width=False)

        if st.button("🔙 กลับไปเลือกรูปอื่น"):
            st.session_state.selected_index = None

    except Exception as e:
        st.error(f"ไม่สามารถโหลดภาพได้: {e}")
        if st.button("🔙 กลับ"):
            st.session_state.selected_index = None
