from ultralytics import YOLO
import os
from PIL import Image

model = YOLO("base_yolo11n.pt")
model.export(format="onnx")

results = model.train(data="datasets/chess.yaml", epochs=10, imgsz=640)