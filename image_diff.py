# Here’s a Python script to compare images in two folders (A and B)
# and move the images that are not present in B into a third folder (C).

import os
import cv2
import shutil

def calculate_hash(image_path):
    """Calculate the hash of an image using perceptual hashing (phash)."""
    image = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)
    if image is None:
        return None
    resized = cv2.resize(image, (8, 8))  # Resize to 8x8
    avg = resized.mean()  # Calculate the average pixel value
    phash = ''.join('1' if pixel > avg else '0' for pixel in resized.flatten())
    return phash

def find_differences(folder_a, folder_b, folder_c):
    """Compare images in folder_a with folder_b and move different images to folder_c."""
    if not os.path.exists(folder_c):
        os.makedirs(folder_c)

    # Generate hashes for all images in folder_b
    hashes_b = set()
    for file in os.listdir(folder_b):
        file_path = os.path.join(folder_b, file)
        if file.lower().endswith(('jpg', 'jpeg', 'png')):
            hash_b = calculate_hash(file_path)
            if hash_b:
                hashes_b.add(hash_b)

    # Compare images in folder_a against folder_b
    for file in os.listdir(folder_a):
        file_path = os.path.join(folder_a, file)
        if file.lower().endswith(('jpg', 'jpeg', 'png')):
            hash_a = calculate_hash(file_path)
            if hash_a and hash_a not in hashes_b:
                shutil.move(file_path, os.path.join(folder_c, file))
                print(f"Moved: {file}")

# Configure paths
folder_a = "/Users/huynhpham/myfolder/FotoApp/imagerest"  # Replace with the path to folder A
folder_b = "/Users/huynhpham/myfolder/FotoApp/imagerest/group_output"  # Replace with the path to folder B
folder_c = "/Users/huynhpham/myfolder/FotoApp/imagerest/checkdiff"  # Replace with the path to folder C (destination)

# Call the function
find_differences(folder_a, folder_b, folder_c)