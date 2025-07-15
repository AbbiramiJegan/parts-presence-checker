import os
import random
import shutil

# Set seed for reproducibility
random.seed(42)

# Source directories
source_images = 'images'
source_labels = 'labels'

# Output directories
output_dir = 'dataset'  # You can change this to 'dataset' to overwrite
splits = ['train', 'val', 'test']
for split in splits:
    os.makedirs(f'{output_dir}/images/{split}', exist_ok=True)
    os.makedirs(f'{output_dir}/labels/{split}', exist_ok=True)

# Get list of image files
image_files = [f for f in os.listdir(source_images) if f.endswith(('.jpg', '.png', '.jpeg'))]
random.shuffle(image_files)

# Split ratios
train_ratio = 0.7
val_ratio = 0.2
test_ratio = 0.1

# Compute split sizes
total = len(image_files)
train_end = int(total * train_ratio)
val_end = train_end + int(total * val_ratio)

train_files = image_files[:train_end]
val_files = image_files[train_end:val_end]
test_files = image_files[val_end:]

def copy_files(file_list, split):
    for file in file_list:
        img_src = os.path.join(source_images, file)
        lbl_src = os.path.join(source_labels, file.rsplit('.', 1)[0] + '.txt')

        img_dst = os.path.join(output_dir, 'images', split, file)
        lbl_dst = os.path.join(output_dir, 'labels', split, file.rsplit('.', 1)[0] + '.txt')

        if os.path.exists(lbl_src):  # Only copy if label exists
            shutil.copyfile(img_src, img_dst)
            shutil.copyfile(lbl_src, lbl_dst)

copy_files(train_files, 'train')
copy_files(val_files, 'val')
copy_files(test_files, 'test')

print(f"Done. Split {total} images into:")
print(f"- Train: {len(train_files)}")
print(f"- Val:   {len(val_files)}")
print(f"- Test:  {len(test_files)}")
