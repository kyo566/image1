import streamlit as st
from PIL import Image
import requests
from io import BytesIO
from ultralytics import YOLO

# โหลดโมเดล YOLOv5s
@st.cache_resource
def load_model():
    return YOLO("yolov5s.pt")

model = load_model()

st.title("🖼️ ตรวจจับวัตถุในภาพด้วย YOLOv5")

method = st.radio("เลือกรูปแบบการใส่ภาพ", ["อัปโหลดไฟล์", "ใส่ URL"])

image = None

if method == "อัปโหลดไฟล์":
    uploaded_file = st.file_uploader("เลือกรูปภาพ", type=["jpg", "jpeg", "png"])
    if uploaded_file:
        image = Image.open(uploaded_file)

elif method == "ใส่ URL":
    url = st.text_input("ป้อน URL ของภาพ")
    if url:
        try:
            response = requests.get(url)
            image = Image.open(BytesIO(response.content))
        except:
            st.error("ไม่สามารถโหลดภาพจาก URL ได้")

if image:
    st.image(image, caption="ภาพต้นฉบับ", use_column_width=True)

    st.write("🔎 กำลังตรวจจับวัตถุ...")
    results = model.predict(image)

    # แสดงผล
    rendered = results[0].plot()
    st.image(rendered, caption="วัตถุที่ตรวจพบ", use_column_width=True)

    # แสดงชื่อวัตถุทั้งหมด
    st.write("📋 รายการวัตถุที่พบ:")
    names = model.names
    labels = [names[int(cls)] for cls in results[0].boxes.cls]
    st.write(labels)
