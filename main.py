from ultralytics import YOLO

# Load YOLOv8 model (pretrained)
model = YOLO("yolov8n.pt")  # Use 'yolov8m.pt' or 'yolov8l.pt' for larger models

# Train the model
model.train(data="dataset/dataset.yaml", epochs=1, imgsz=640, batch=16)
