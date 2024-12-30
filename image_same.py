import os
import cv2
import shutil
import numpy as np

def calculate_similarity(img1, img2):
    """Tính độ tương đồng giữa hai ảnh bằng ORB và FLANN-based matcher."""
    img1 = cv2.resize(img1, (1000, 1000))
    img2 = cv2.resize(img2, (1000, 1000))
    orb = cv2.ORB_create(nfeatures=2000)

    # Phát hiện và mô tả đặc trưng
    keypoints1, descriptors1 = orb.detectAndCompute(img1, None)
    keypoints2, descriptors2 = orb.detectAndCompute(img2, None)

    # Sử dụng FLANN-based matcher để so sánh đặc trưng
    index_params = dict(algorithm=6, table_number=6, key_size=12, multi_probe_level=1)
    search_params = dict(checks=50)
    flann = cv2.FlannBasedMatcher(index_params, search_params)

    if descriptors1 is None or descriptors2 is None:
        return 0  # Không có đặc trưng nào để so sánh

    matches = flann.knnMatch(descriptors1, descriptors2, k=2)

    # Áp dụng ratio test
    good_matches = [m for m in matches if len(m) == 2 and m[0].distance < 0.6 * m[1].distance]
    return len(good_matches)

def group_similar_images(image_folder, output_folder, similarity_threshold=10):
    """Nhóm các ảnh gần giống nhau vào các thư mục."""
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    images = [f for f in os.listdir(image_folder) if f.lower().endswith(('jpg', 'jpeg', 'png'))]

    grouped = []

    group_count = 0  # Đếm số nhóm

    for image_file in images:
        print(f"Working on {image_file}")
        #  handle corrupt JPEG data: bad Huffman code
        # try:
        #     img1 = cv2.imread(image_file, cv2.IMREAD_GRAYSCALE)
        #     if img1 is None:
        #         raise ValueError(f"Cannot read image: {image_file}")
        # except Exception as e:
        #     print(f"Error reading image {image_file}: {e}")
        #     continue  # Bỏ qua ảnh lỗi

        if image_file in grouped:
            continue

        image_path = os.path.join(image_folder, image_file)
        img1 = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)

        # Tạo nhóm mới
        group_count += 1
        group_dir = os.path.join(output_folder, f"group_{group_count}")
        os.makedirs(group_dir, exist_ok=True)
        shutil.copy(image_path, group_dir)
        grouped.append(image_file)

        for other_image in images:
            if other_image in grouped:
                continue

            other_image_path = os.path.join(image_folder, other_image)
            img2 = cv2.imread(other_image_path, cv2.IMREAD_GRAYSCALE)
            similarity = calculate_similarity(img1, img2)

            # Nhóm ảnh chỉ nếu độ tương đồng đạt ngưỡng
            if similarity >= similarity_threshold:
                shutil.copy(other_image_path, group_dir)
                grouped.append(other_image)

        # Nếu chỉ có một ảnh trong nhóm thì đổi tên nhóm thành "single"
        if len(os.listdir(group_dir)) == 1:
            image_single = os.path.join(group_dir, image_file)
            shutil.copy(image_single, output_single)

        print(f"Group {group_count} created with images: {os.listdir(group_dir)}")

def delete_single_file_folders(source_folder):
    """
    Xóa các thư mục con chỉ chứa một thành phần trong thư mục nguồn.

    Args:
        source_folder (str): Đường dẫn đến thư mục nguồn.
    """

    for folder in os.listdir(source_folder):
        folder_path = os.path.join(source_folder, folder)
        if os.path.isdir(folder_path):  # Kiểm tra xem là thư mục
            contents = os.listdir(folder_path)
            if len(contents) == 1:  # Nếu chỉ có một thành phần
                shutil.rmtree(folder_path)
                print(f"Đã xóa thư mục: {folder_path}")
# # Cấu hình đường dẫn
image_folder = "/Users/huynhpham/myfolder/FotoApp/imagerest"
output_folder = "/Users/huynhpham/myfolder/FotoApp/imagerest/group_output"
output_single = "/Users/huynhpham/myfolder/FotoApp/imagerest/group_output/single"

# image_folder = "/Users/huynhpham/myfolder/FotoApp/test"
# output_folder = "/Users/huynhpham/myfolder/FotoApp/test/group_output"
# output_single = "/Users/huynhpham/myfolder/FotoApp/test/group_output/single"
group_similar_images(image_folder, output_folder)
delete_single_file_folders(output_folder)