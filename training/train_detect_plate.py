from ultralytics import YOLO
# model = YOLO("yolov8l.pt")
# model.train(data="dataset.yaml", epochs=30, batch=8, workers=4, degrees=90.0)
model = YOLO('./runs/detect/train/weights/last.pt')
model.predict("../images/9e0676c9539b0104cb5862e8f6b4d93e.jpg",save=True, conf=0.2, iou=0.5)