import os

# Set your image folder path here
folder_path = "."

# Get all files in the folder and sort them
files = sorted(os.listdir(folder_path))

# Filter only image files (optional - based on common extensions)
image_extensions = ('.jpg', '.jpeg', '.png', '.gif', '.bmp', '.tiff', '.webp')
image_files = [f for f in files if f.lower().endswith(image_extensions)]

# Rename images to 1.jpg, 2.jpg, etc.
for index, filename in enumerate(image_files, start=1):
    ext = os.path.splitext(filename)[1]  # Get file extension
    new_name = f"{index}{ext}"
    src = os.path.join(folder_path, filename)
    dst = os.path.join(folder_path, new_name)
    os.rename(src, dst)
    print(f"Renamed '{filename}' to '{new_name}'")

print("Renaming complete.")
