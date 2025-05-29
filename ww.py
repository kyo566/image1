import streamlit as st
from PIL import Image
import requests
from io import BytesIO
import torch
import torchvision.transforms as T

# โหลดโมเดล pretrained Faster R-CNN จาก torchvision
model = torch.hub.load('pytorch/vision:v0.15.2', 'fasterrcnn_resnet50_fpn', pretrained=True)
model.eval()

# รายชื่อ class ของ COCO dataset (โมเดลถูกฝึกด้วย COCO)
COCO_INSTANCE_CATEGORY_NAMES = [
    '__background__', 'person', 'bicycle', 'car', 'motorcycle', 'airplane', 'bus',
    'train', 'truck', 'boat', 'traffic light', 'fire hydrant', 'stop sign',
    'parking meter', 'bench', 'bird', 'cat', 'dog', 'horse', 'sheep', 'cow',
    'elephant', 'bear', 'zebra', 'giraffe', 'backpack', 'umbrella', 'handbag',
    'tie', 'suitcase', 'frisbee', 'skis', 'snowboard', 'sports ball', 'kite',
    'baseball bat', 'baseball glove', 'skateboard', 'surfboard', 'tennis racket',
    'bottle', 'wine glass', 'cup', 'fork', 'knife', 'spoon', 'bowl', 'banana',
    'apple', 'sandwich', 'orange', 'broccoli', 'carrot', 'hot dog', 'pizza',
    'donut', 'cake', 'chair', 'couch', 'potted plant', 'bed', 'dining table',
    'toilet', 'tv', 'laptop', 'mouse', 'remote', 'keyboard', 'cell phone',
    'microwave', 'oven', 'toaster', 'sink', 'refrigerator', 'book', 'clock',
    'vase', 'scissors', 'teddy bear', 'hair drier', 'toothbrush'
]

def load_image_from_url(url):
    response = requests.get(url)
    img = Image.open(BytesIO(response.content)).convert("RGB")
    return img

def transform_image(img):
    transform = T.Compose([
        T.ToTensor()
    ])
    return transform(img)

def get_prediction(img, threshold=0.5):
    # แปลงภาพ
    img_t = transform_image(img)
    with torch.no_grad():
        predictions = model([img_t])
    pred_classes = [COCO_INSTANCE_CATEGORY_NAMES[i] for i in list(predictions[0]['labels'].numpy())]
    pred_scores = list(predictions[0]['scores'].numpy())
    # กรองตาม threshold
    pred_t = [pred_scores.index(x) for x in pred_scores if x > threshold]
    if pred_t:
        pred_t = pred_t[-1]  # index ตัวสุดท้ายที่ผ่าน threshold
        pred_classes = pred_classes[:pred_t+1]
    else:
        pred_classes = []
    return set(pred_classes)

# Streamlit UI
st.title("Object Detection in Image")

option = st.radio("Choose image input method:", ('Upload image', 'Image URL'))

if option == 'Upload image':
    uploaded_file = st.file_uploader("Upload an image", type=["jpg", "jpeg", "png"])
    if uploaded_file is not None:
        img = Image.open(uploaded_file).convert("RGB")
        st.image(img, caption='Uploaded Image', use_column_width=True)
        objects = get_prediction(img)
        if objects:
            st.write("Detected objects:")
            for obj in objects:
                st.write("- " + obj)
        else:
            st.write("No objects detected with high confidence.")

else:
    url = st.text_input("Enter image URL:")
    if url:
        try:
            img = load_image_from_url(url)
            st.image(img, caption='Image from URL', use_column_width=True)
            objects = get_prediction(img)
            if objects:
                st.write("Detected objects:")
                for obj in objects:
                    st.write("- " + obj)
            else:
                st.write("No objects detected with high confidence.")
        except Exception as e:
            st.error(f"Could not load image from URL: {e}")
