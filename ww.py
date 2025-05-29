import streamlit as st
import requests
from PIL import Image
from io import BytesIO

API_KEY = 'your_roboflow_api_key'
MODEL_URL = 'https://detect.roboflow.com/YOUR-MODEL/1?api_key=' + API_KEY

def detect_objects(image):
    buffered = BytesIO()
    image.save(buffered, format="JPEG")
    img_bytes = buffered.getvalue()
    response = requests.post(MODEL_URL, files={"file": img_bytes})
    return response.json()

st.title("Detect objects with Roboflow API")

uploaded_file = st.file_uploader("Upload an image", type=["jpg", "jpeg", "png"])
if uploaded_file:
    img = Image.open(uploaded_file)
    st.image(img, caption="Uploaded Image")

    result = detect_objects(img)
    st.write(result)
