import streamlit as st
from PIL import Image
import requests
from io import BytesIO
from ultralytics import YOLO

# โหลดโมเดล YOLOv8 Nano (เล็กสุด เร็ว)
model = YOLO('yolov8n.pt')

def load_image_from_url(url):
    response = requests.get(url)
    response.raise_for_status()  # ตรวจสอบว่าดึงภาพได้หรือไม่
    img = Image.open(BytesIO(response.content)).convert("RGB")
    return img

st.title("Object Detection with YOLOv8 and Streamlit")

input_method = st.radio("เลือกวิธีใส่ภาพ", ("Upload Image", "Image URL"))

if input_method == "Upload Image":
    uploaded_file = st.file_uploader("อัปโหลดไฟล์ภาพ", type=["jpg", "jpeg", "png"])
    if uploaded_file:
        image = Image.open(uploaded_file).convert("RGB")
        st.image(image, caption="Uploaded Image", use_column_width=True)

        results = model(image)
        labels = results[0].names
        detected = set()
        for box in results[0].boxes:
            cls = int(box.cls[0])
            detected.add(labels[cls])

        if detected:
            st.markdown("**Detected objects:**")
            for obj in detected:
                st.write("- " + obj)
        else:
            st.write("ไม่พบวัตถุในภาพ")

elif input_method == "Image URL":
    url = st.text_input("ใส่ URL ของภาพ")
    if url:
        try:
            image = load_image_from_url(url)
            st.image(image, caption="Image from URL", use_column_width=True)

            results = model(image)
            labels = results[0].names
            detected = set()
            for box in results[0].boxes:
                cls = int(box.cls[0])
                detected.add(labels[cls])

            if detected:
                st.markdown("**Detected objects:**")
                for obj in detected:
                    st.write("- " + obj)
            else:
                st.write("ไม่พบวัตถุในภาพ")
        except Exception as e:
            st.error(f"โหลดภาพไม่สำเร็จ: {e}")
