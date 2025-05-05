from ultralytics import YOLO
import os
from PIL import Image

model = YOLO("../assets/base_yolo11n.pt")
model.export(format="onnx")

results = model.train(data="chess.yaml", epochs=150, imgsz=640)