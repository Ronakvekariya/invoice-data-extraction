"""YOLOv8 training entry point for invoice field detection."""

import argparse

from ultralytics import YOLO


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Train a YOLOv8 model for invoice field detection."
    )
    parser.add_argument("--data", default="path/to/dataset.yaml")
    parser.add_argument("--model", default="yolov8n.pt")
    parser.add_argument("--epochs", type=int, default=1)
    parser.add_argument("--imgsz", type=int, default=640)
    parser.add_argument("--batch", type=int, default=16)
    args = parser.parse_args()

    model = YOLO(args.model)
    model.train(
        data=args.data,
        epochs=args.epochs,
        imgsz=args.imgsz,
        batch=args.batch,
    )


if __name__ == "__main__":
    main()
