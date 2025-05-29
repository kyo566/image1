import streamlit as st
from PIL import Image, ImageDraw
import requests
from io import BytesIO
import base64

st.set_page_config(page_title="ภาพพร้อมกรอบไม้บรรทัด", layout="wide")
st.title("✂️ แสดงภาพพร้อมกรอบไม้บรรทัดแบบโปรแกรมตัดต่อ")

# URLs ของภาพ
image_urls = [
    "https://cdn.pixabay.com/photo/2024/05/26/10/15/bird-8788491_1280.jpg",
    "https://cdn.pixabay.com/photo/2018/09/24/08/52/mountains-3699372_1280.jpg",
    "https://cdn.pixabay.com/photo/2019/10/14/03/26/landscape-4547734_1280.jpg"
]

# ใช้ session_state เก็บสถานะ
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

    bg = Image.new("RGB", (new_width, new_height), color="#f0f0f0")
    bg.paste(image, (margin, margin))

    draw = ImageDraw.Draw(bg)

    # ไม้บรรทัดด้านบน (X)
    for x in range(0, width, step):
        pos = x + margin
        draw.line([(pos, margin - 15), (pos, margin)], fill="black", width=1)
        draw.text((pos + 2, 2), str(x), fill="black")

    # ไม้บรรทัดด้านซ้าย (Y)
    for y in range(0, height, step):
        pos = y + margin
        draw.line([(margin - 15, pos), (margin, pos)], fill="black", width=1)
        draw.text((2, pos - 7), str(y), fill="black")

    return bg

# หน้าเลือกภาพ
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
                st.error(f"โหลดภาพไม่สำเร็จ: {e}")

# หน้าแสดงภาพเดี่ยว
else:
    selected_url = image_urls[st.session_state.selected_index]
    try:
        response = requests.get(selected_url)
        response.raise_for_status()
        image = Image.open(BytesIO(response.content))

        col1, col2 = st.columns(2)
        with col1:
            width = st.slider("ความกว้าง (X)", 100, 1000, st.session_state.image_width, 50)
        with col2:
            height = st.slider("ความสูง (Y)", 100, 1000, st.session_state.image_height, 50)

        st.session_state.image_width = width
        st.session_state.image_height = height

        resized = image.resize((width, height))
        final_img = draw_ruler_frame(resized, step=50, margin=40)

        # แปลงภาพเป็น data URI สำหรับ HTML
        buffer = BytesIO()
        final_img.save(buffer, format="PNG")
        img_bytes = buffer.getvalue()
        img_data_uri = f"data:image/png;base64,{base64.b64encode(img_bytes).decode()}"

        # แสดงภาพกลางหน้าจอแบบมีกรอบ/เงา
        st.markdown(
            f"""
            <div style="display: flex; justify-content: center; padding: 30px;">
                <img src="{img_data_uri}" style="box-shadow: 0px 0px 20px rgba(0,0,0,0.25); border: 1px solid #ccc;" />
            </div>
            """,
            unsafe_allow_html=True
        )

        if st.button("🔙 กลับไปเลือกรูปอื่น"):
            st.session_state.selected_index = None

    except Exception as e:
        st.error(f"โหลดภาพไม่สำเร็จ: {e}")
        if st.button("🔙 กลับ"):
            st.session_state.selected_index = None
