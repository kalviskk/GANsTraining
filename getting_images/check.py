import os
from PIL import Image
import numpy as np
from concurrent.futures import ThreadPoolExecutor

def is_color_in_image(image_path, colors_to_check):
    try:
        with Image.open(image_path) as img:
            img = img.convert('RGB')
            data = np.array(img)

            # Check if any of the specified colors are in the image
            for color in colors_to_check:
                if np.any(np.all(data == color, axis=-1)):
                    return True
            return False
    except Exception as e:
        print(f"Error processing {image_path}: {e}")
        return False

def check_colors_in_directory(directory, colors_to_check):
    files_with_color = []
    with ThreadPoolExecutor() as executor:
        futures = {executor.submit(is_color_in_image, os.path.join(directory, filename), colors_to_check): filename for filename in os.listdir(directory) if filename.lower().endswith(('.png', '.jpg', '.jpeg'))}

        for future in futures:
            if future.result():
                files_with_color.append(futures[future])
                print(f"Color found in {futures[future]}")

    return files_with_color


# Specify the directory and the colors to check
directory = "mapbox_images2/roadmap"
colors_to_check = [(255, 255, 255), (223, 215, 212), (210, 210, 210), (211, 211, 211), (212, 212, 212),
                   (213, 213, 213), (214, 214, 214), (215, 215, 215), (216, 216, 216),
                   (217, 217, 217), (218, 218, 218), (219, 219, 219), (220, 220, 220)]


files_with_specified_color = check_colors_in_directory(directory, colors_to_check)
print(f"Files with the specified color: {files_with_specified_color}")



#%%

import os

# Array of filenames that should not be deleted
valid_filenames = os.listdir(r"C:\Users\kalvi\Desktop\skola\2.kurss\ML\projekts\mapbox_images2\satellite_processed")
# Replace with names of files you want to keep

directory_path = r"C:\Users\kalvi\Desktop\skola\2.kurss\ML\projekts\mapbox_images2\satellite"  # Replace with the path to your directory

# Loop through all files in the directory
for filename in os.listdir(directory_path):
    # Construct the full file path
    file_path = os.path.join(directory_path, filename)

    # Check if the file is not in the list of valid filenames
    if filename in valid_filenames:
        # Delete the file
        os.remove(file_path)
        print(f"Deleted {filename}")

# Print completion message
print("File cleanup complete.")

#%%
import re

roadmap_directory = r"C:\Users\kalvi\Desktop\skola\2.kurss\ML\projekts\mapbox_images2\roadmap - Copy"
satellite_directory = r"C:\Users\kalvi\Desktop\skola\2.kurss\ML\projekts\mapbox_images2\satellite - Copy"
# Regex pattern to extract coordinates
pattern = re.compile(r"_(\d+_\d+_\d+_\d+)\.jpg")

# Set to store coordinates of roadmap images
roadmap_coords = set()

# Read all roadmap filenames and store their coordinates
for filename in os.listdir(roadmap_directory):
    match = pattern.search(filename)
    if match:
        # Add coordinates to the set
        roadmap_coords.add(match.group(1))

# Loop through satellite images and delete if no corresponding roadmap image
for filename in os.listdir(satellite_directory):
    match = pattern.search(filename)
    if match:
        coord = match.group(1)
        if coord not in roadmap_coords:
            # Construct full file path
            file_path = os.path.join(satellite_directory, filename)
            # Delete the file
            os.remove(file_path)
            print(f"Deleted {filename}")

print("File cleanup complete.")
