import os
import json
import numpy as np
from PIL import Image
from tensorflow.keras.applications import MobileNetV2
from tensorflow.keras.applications.mobilenet_v2 import preprocess_input, decode_predictions

# Load mô hình pre-trained
model = MobileNetV2(weights='imagenet')

def analyze_image(image_path):
    """Phân tích ảnh và trả về các object nhận diện được."""
    image = Image.open(image_path).resize((224, 224))
    img_array = np.array(image)
    img_array = preprocess_input(img_array)
    img_array = np.expand_dims(img_array, axis=0)

    predictions = model.predict(img_array)
    decoded_predictions = decode_predictions(predictions, top=3)[0]  # Top 3 predictions

    # Chuyển đổi `prob` từ float32 sang float
    return [(label, float(prob)) for (_, label, prob) in decoded_predictions]

def process_images(image_folder, output_file):
    """Phân tích và lưu kết quả nhãn vào file JSON."""
    results = {}

    for image_file in os.listdir(image_folder):
        image_path = os.path.join(image_folder, image_file)
        if os.path.isfile(image_path) and image_path.lower().endswith(('jpg', 'jpeg', 'png')):
            print(f"Analyzing: {image_file}")
            labels = analyze_image(image_path)
            results[image_file] = labels

    with open(output_file, "w") as f:
        json.dump(results, f, indent=4)
    print(f"Results saved to {output_file}")

# Phân tích tất cả ảnh trong thư mục
image_folder = "/Users/huynhpham/myfolder/FotoApp/imagerest"
output_file = "image_labels.json"
process_images(image_folder, output_file)
#  các object này ngu quá


#  search

# def search_images(keyword, labels_file):
#     """Tìm kiếm các ảnh chứa từ khóa."""
#     with open(labels_file, "r") as f:
#         data = json.load(f)

#     results = []
#     for image, labels in data.items():
#         if any(keyword in label for label, _ in labels):
#             results.append(image)

#     return results

# Tìm kiếm từ khóa
# keyword = "mountain_bike"
# found_images = search_images(keyword, output_file)
# print(f"Images containing '{keyword}': {found_images}")