import cv2
import os
import shutil

def detect_and_match_faces(source_folder, reference_image_path, target_folder, threshold=0.5):
    """
    Phát hiện khuôn mặt trong ảnh từ source_folder,
    so sánh với khuôn mặt trong reference_image_path,
    và sao chép ảnh có khuôn mặt giống nhau vào target_folder.
    """
    if not os.path.exists(target_folder):
        os.makedirs(target_folder)

    # Load ảnh tham chiếu (ảnh B) và phát hiện khuôn mặt
    reference_image = cv2.imread(reference_image_path)
    if reference_image is None:
        print(f"Không thể đọc ảnh tham chiếu: {reference_image_path}")
        return

    face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
    gray_reference = cv2.cvtColor(reference_image, cv2.COLOR_BGR2GRAY)
    reference_faces = face_cascade.detectMultiScale(gray_reference, scaleFactor=1.05, minNeighbors=30, minSize=(30, 30))

    if len(reference_faces) == 0:
        print(f"Không tìm thấy khuôn mặt trong ảnh tham chiếu: {reference_image_path}")
        return

    # Chỉ lấy khuôn mặt đầu tiên trong ảnh tham chiếu
    x, y, w, h = reference_faces[0]
    reference_face = gray_reference[y:y+h, x:x+w]
    reference_face = cv2.resize(reference_face, (100, 100))

    # Duyệt qua các ảnh trong thư mục nguồn
    for image_file in os.listdir(source_folder):
        if image_file.lower().endswith(('jpg', 'jpeg', 'png')):
            image_path = os.path.join(source_folder, image_file)
            image = cv2.imread(image_path)

            if image is None:
                print(f"Không thể đọc ảnh: {image_path}")
                continue

            gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
            faces = face_cascade.detectMultiScale(gray_image, scaleFactor=1.05, minNeighbors=30, minSize=(30, 30))

            for (x, y, w, h) in faces:
                detected_face = gray_image[y:y+h, x:x+w]
                detected_face = cv2.resize(detected_face, (100, 100))

                # Tính toán độ tương đồng giữa khuôn mặt tham chiếu và khuôn mặt phát hiện
                similarity = cv2.norm(reference_face, detected_face, cv2.NORM_L2) / (100 * 100)
                if similarity < threshold:  # Độ tương đồng thấp nghĩa là giống nhau
                    print(f"Phát hiện khuôn mặt giống nhau trong ảnh: {image_file}")
                    target_path = os.path.join(target_folder, image_file)
                    shutil.copy(image_path, target_path)
                    break

# Cấu hình đường dẫn
source_folder = "/Users/huynhpham/myfolder/FotoApp/detectface/src"  # Thư mục A
reference_image_path = "/Users/huynhpham/myfolder/FotoApp/detectface/NTP_1215.jpg"  # Ảnh B
target_folder = "/Users/huynhpham/myfolder/FotoApp/detectface/target"  # Thư mục đích

# Gọi hàm
detect_and_match_faces(source_folder, reference_image_path, target_folder)