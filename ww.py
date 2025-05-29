import streamlit as st
from PIL import Image
import requests
from io import BytesIO
from ultralytics import YOLO

model = YOLO('yolov8n.pt')  # โหลดโมเดล YOLOv8 Nano (เล็กสุด)

def load_image_from_url(url):
    response = requests.get(url)
    img = Image.open(BytesIO(response.content)).convert("RGB")
    return img

st.title("YOLOv8 Object Detection with Streamlit")

option = st.radio("Input method:", ['Upload Image', 'Image URL'])

if option == 'Upload Image':
    uploaded_file = st.file_uploader("Upload an image", type=['jpg', 'jpeg', 'png'])
    if uploaded_file:
        img = Image.open(uploaded_file).convert("RGB")
        st.image(img, caption="Uploaded Image", use_column_width=True)
        results = model(img)
        labels = results[0].names
        detected = set()
        for box in results[0].boxes:
            cls = int(box.cls[0])
            detected.add(labels[cls])
        if detected:
            st.write("Detected objects:")
            for obj in detected:
                st.write("- " + obj)
        else:
            st.write("No objects detected.")
elif option == 'Image URL':
    url = st.text_input("Enter image URL:")
    if url:
        try:
            img = load_image_from_url(url)
            st.image(img, caption="Image from URL", use_column_width=True)
            results = model(img)
            labels = results[0].names
            detected = set()
            for box in results[0].boxes:
                cls = int(box.cls[0])
                detected.add(labels[cls])
            if detected:
                st.write("Detected objects:")
                for obj in detected:
                    st.write("- " + obj)
            else:
                st.write("No objects detected.")
        except Exception as e:
            st.error(f"Cannot load image from URL: {e}")
