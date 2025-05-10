import torch
from ultralytics import YOLO

torch.cuda.set_device(0) # Verify gpu is available

model = YOLO("../assets/base_yolo11n.pt")
results = model.train(data="chess.yaml", epochs=150, batch=32, imgsz=800, device=0)