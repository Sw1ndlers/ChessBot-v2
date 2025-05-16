from PIL import Image, ImageDraw

def draw_yolo_bboxes(image_file, label_file):
    # Load the image
    image = Image.open(image_file)
    draw = ImageDraw.Draw(image)

    # Read the YOLO label file
    with open(label_file, 'r') as file:
        labels = file.readlines()

    # For each label, draw the bounding box
    for label in labels:
        parts = label.strip().split()
        class_id = int(parts[0])
        x_center = float(parts[1])
        y_center = float(parts[2])
        width = float(parts[3])
        height = float(parts[4])

        # Convert YOLO coordinates to pixel coordinates
        image_width, image_height = image.size
        x_min = int((x_center - width / 2) * image_width)
        y_min = int((y_center - height / 2) * image_height)
        x_max = int((x_center + width / 2) * image_width)
        y_max = int((y_center + height / 2) * image_height)

        # Draw the bounding box (red for visibility)
        draw.rectangle([x_min, y_min, x_max, y_max], outline="red", width=3)

    # Save the image with bounding boxes
    image.show()

# Example usage
image_file = r'datasets\chess_yolo_dataset\train\images\output_0.png'
label_file = r'datasets\chess_yolo_dataset\train\labels\output_0.txt'
draw_yolo_bboxes(image_file, label_file)