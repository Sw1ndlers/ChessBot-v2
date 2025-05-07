import torch
from ultralytics import YOLO

torch.cuda.set_device(0) # Comment out this line if you want to use CPU

model = YOLO("../assets/base_yolo11n.pt")
# model.export(format="onnx")

results = model.train(data="chess.yaml", epochs=150, batch=32, imgsz=800, device=0)