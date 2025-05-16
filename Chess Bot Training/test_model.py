from ultralytics import YOLO
import cv2

model = YOLO("../assets/best.onnx")  # Just point to your ONNX model

# load and convert image to 800x800
img = cv2.imread("test_image.png")
img = cv2.resize(img, (img.shape[1] // 2, img.shape[0] // 2))

results = model.predict(source=img, task="detect")

result = results[0]

conf_threshold = 0.95
filtered_boxes = result.boxes[result.boxes.conf > conf_threshold]

result.boxes = filtered_boxes

img = result.plot(line_width=1, font_size=0.4)  # Smaller boxes + text

# Show it using OpenCV
cv2.imshow("Result", img)
cv2.waitKey(0)
cv2.destroyAllWindows()