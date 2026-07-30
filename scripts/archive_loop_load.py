import zipfile
import os

# 1. Base files directory
base_dir = "/lakehouse/default/Files"

# 2. Automatically find the shortcut directory that starts with "wmpp-production"
shortcut_folder = [f for f in os.listdir(base_dir) if f.startswith("wmpp-production")][0]

# 3. Construct the exact POSIX path to the archive folder
archive_dir = os.path.join(base_dir, shortcut_folder, "archive")
extract_path = os.path.join(base_dir, "archive_unzipped")

os.makedirs(extract_path, exist_ok=True)

# 4. Unzip all daily archives
zip_files = [f for f in os.listdir(archive_dir) if f.endswith('.zip')]
print(f"Found {len(zip_files)} zip files in {archive_dir}")

for filename in zip_files:
    file_path = os.path.join(archive_dir, filename)
    with zipfile.ZipFile(file_path, 'r') as zip_ref:
        zip_ref.extractall(extract_path)

print(f"Successfully unzipped all files into: {extract_path}")
