from ultralytics import YOLO
import cv2

model = YOLO("best.onnx")  # Just point to your ONNX model
results = model("test_image.jpg")

# Get annotated image (NumPy array)
img = results[0].plot(line_width=1, font_size=0.4)  # Smaller boxes + text

# Show it using OpenCV
cv2.imshow("Result", img)
cv2.waitKey(0)
cv2.destroyAllWindows()