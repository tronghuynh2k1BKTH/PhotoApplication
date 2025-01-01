# convert .webp to .jpeg

from PIL import Image
import os

def convert_webp_to_jpeg(input_folder, output_folder):
    """Convert all .webp files in the input folder to .jpeg files in the output folder, and delete the original .webp files."""
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    for file_name in os.listdir(input_folder):
        if file_name.lower().endswith('.webp'):
            input_path = os.path.join(input_folder, file_name)
            output_file_name = file_name.replace('.webp', '.jpeg')  # Ensure proper file naming
            output_path = os.path.join(output_folder, output_file_name)

            try:
                with Image.open(input_path) as img:
                    img = img.convert("RGB")  # Convert to RGB format for JPEG
                    img.save(output_path, "JPEG")
                    print(f"Converted: {file_name} -> {output_path}")

                # Delete the original .webp file
                os.remove(input_path)
                print(f"Deleted original file: {input_path}")

            except Exception as e:
                print(f"Failed to convert {file_name}: {e}")

# Configure paths
input_folder = "/Users/huynhpham/myfolder/FotoApp/imagerest"   # Replace with the folder containing .webp files

# Call the function
convert_webp_to_jpeg(input_folder, input_folder)