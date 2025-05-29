import streamlit as st
import requests
from PIL import Image
from io import BytesIO
import torch

# โหลดโมเดล YOLOv5 (ใช้ yolov5s ที่เบาที่สุด)
@st.cache_resource
def load_model():
    return torch.hub.load('ultralytics/yolov5', 'yolov5s', pretrained=True)

model = load_model()

st.title("🔍 ตรวจจับวัตถุในภาพด้วย YOLOv5")

option = st.radio("เลือกวิธีการใส่รูปภาพ", ("📤 อัปโหลดไฟล์", "🌐 ใส่ URL"))

image = None

if option == "📤 อัปโหลดไฟล์":
    uploaded_file = st.file_uploader("อัปโหลดรูปภาพ", type=["jpg", "jpeg", "png"])
    if uploaded_file:
        image = Image.open(uploaded_file)

elif option == "🌐 ใส่ URL":
    url = st.text_input("ใส่ URL ของภาพ")
    if url:
        try:
            response = requests.get(url)
            image = Image.open(BytesIO(response.content))
        except:
            st.error("ไม่สามารถโหลดภาพจาก URL ได้")

if image:
    st.image(image, caption="ภาพต้นฉบับ", use_column_width=True)

    st.write("🔎 กำลังประมวลผล...")
    results = model(image)

    # แสดงภาพพร้อมกรอบ
    st.image(results.render()[0], caption="วัตถุที่ตรวจพบ", use_column_width=True)

    # แสดงรายละเอียดวัตถุที่เจอ
    df = results.pandas().xyxy[0]
    st.write("📋 วัตถุที่ตรวจพบ:")
    st.dataframe(df[['name', 'confidence']])
