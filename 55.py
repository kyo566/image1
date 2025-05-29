import streamlit as st
from PIL import Image
import requests
from io import BytesIO

st.set_page_config(page_title="แสดงภาพนกจาก Pixabay", layout="wide")
st.title("🕊️ แสดงภาพนกจาก Pixabay")

# รายการ URL ของภาพ
image_urls = [
    "https://cdn.pixabay.com/photo/2024/05/26/10/15/bird-8788491_1280.jpg",
    "https://cdn.pixabay.com/photo/2018/09/24/08/52/mountains-3699372_1280.jpg",
    "https://cdn.pixabay.com/photo/2019/10/14/03/26/landscape-4547734_1280.jpg"
]

# กำหนดค่าเริ่มต้นใน session state
if "selected_index" not in st.session_state:
    st.session_state.selected_index = None

if "image_width" not in st.session_state:
    st.session_state.image_width = 300

# แสดงภาพเรียงใน 3 คอลัมน์
cols = st.columns(3)

for idx, url in enumerate(image_urls):
    with cols[idx]:
        try:
            response = requests.get(url)
            response.raise_for_status()
            content_type = response.headers.get("Content-Type", "")
            if "image" not in content_type:
                raise ValueError(f"URL นี้ไม่ได้ส่งคืนรูปภาพ: {content_type}")
            image = Image.open(BytesIO(response.content))

            st.image(image, caption=f"ภาพที่ {idx+1}", use_container_width=True)
            if st.button(f"เลือกภาพที่ {idx+1}", key=f"btn_{idx}"):
                st.session_state.selected_index = idx
        except Exception as e:
            st.error(f"โหลดภาพที่ {idx+1} ไม่สำเร็จ: {e}")

# ถ้ามีการเลือกภาพ
if st.session_state.selected_index is not None:
    st.markdown("---")
    st.subheader(f"🖼️ ปรับขนาดภาพที่ {st.session_state.selected_index + 1}")
    selected_url = image_urls[st.session_state.selected_index]

    try:
        response = requests.get(selected_url)
        response.raise_for_status()
        image = Image.open(BytesIO(response.content))

        # สไลเดอร์สำหรับปรับขนาด
        width = st.slider("ความกว้างของภาพ (px)", min_value=100, max_value=800,
                          value=st.session_state.image_width, step=50)
        st.session_state.image_width = width

        st.image(image, caption="ภาพที่เลือก", width=width)

    except Exception as e:
        st.error(f"ไม่สามารถโหลดภาพที่เลือกได้: {e}")
