import zipfile
import os

# POSIX path to the zip file inside your S3 shortcut
zip_shortcut_path = "/lakehouse/default/Files/my_s3_shortcut/archive.zip"

# Target path (either in OneLake or local Spark node memory/disk)
extract_path = "/lakehouse/default/Files/unzipped_data/"

os.makedirs(extract_path, exist_ok=True)

# Unzip using standard Python library
with zipfile.ZipFile(zip_shortcut_path, 'r') as zip_ref:
    zip_ref.extractall(extract_path)

print("Successfully unzipped files from the S3 shortcut!")
