import streamlit as st
from PIL import Image
import requests
from io import BytesIO
from ultralytics import YOLO

# โหลดโมเดล YOLOv5s
model = YOLO("yolov8n.pt")

st.title("🔍 ตรวจจับวัตถุในภาพ (Object Detection)")

# โหมดการเลือกภาพ
mode = st.radio("เลือกวิธีการนำเข้าภาพ", ["📤 Upload", "🌐 URL"])

image = None

# โหลดภาพจาก upload
if mode == "📤 Upload":
    uploaded_file = st.file_uploader("อัปโหลดภาพ", type=["jpg", "jpeg", "png"])
    if uploaded_file is not None:
        image = Image.open(uploaded_file)

# โหลดภาพจาก URL
elif mode == "🌐 URL":
    url = st.text_input("ใส่ URL ของภาพ")
    if url:
        try:
            response = requests.get(url)
            image = Image.open(BytesIO(response.content))
        except Exception as e:
            st.error(f"ไม่สามารถโหลดภาพจาก URL ได้: {e}")

# แสดงภาพและวิเคราะห์
if image:
    st.image(image, caption="📷 ภาพต้นฉบับ", use_container_width=True)

    with st.spinner("กำลังตรวจจับวัตถุ..."):
        model = YOLO("yolov8n.pt")
        results = model.predict(image)

        result = results[0]
        names = model.names
        detected = set()
        for box in result.boxes:
            cls_id = int(box.cls[0])
            detected.add(names[cls_id])

        st.success("✅ ตรวจจับวัตถุสำเร็จแล้ว")
        st.write("### 🔍 พบวัตถุดังนี้:")
        for obj in detected:
            st.markdown(f"- {obj}")

        st.image(result.plot(), caption="📦 ภาพพร้อมกล่อง", use_container_width=True)
