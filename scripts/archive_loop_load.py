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





import zipfile
import os

# 1. Define paths
base_dir = "/lakehouse/default/Files"

# Automatically find the shortcut folder
shortcut_folder = [f for f in os.listdir(base_dir) if f.startswith("wmpp-production")][0]
archive_dir = os.path.join(base_dir, shortcut_folder, "archive")
extract_path = os.path.join(base_dir, "archive_unzipped")

os.makedirs(extract_path, exist_ok=True)

# 2. Find all ZIP files
zip_files = [f for f in os.listdir(archive_dir) if f.endswith('.zip')]
print(f"Found {len(zip_files)} ZIP archive(s) to check.\n")

extracted_count = 0
skipped_count = 0

# 3. Loop through each ZIP file and inspect individual contents
for zip_name in zip_files:
    zip_file_path = os.path.join(archive_dir, zip_name)
    
    with zipfile.ZipFile(zip_file_path, 'r') as zip_ref:
        for member in zip_ref.infolist():
            # Skip folder objects inside the zip
            if member.is_dir():
                continue
            
            # Destination path of the file
            target_file_path = os.path.join(extract_path, member.filename)
            
            # Extract ONLY if the file doesn't exist yet
            if os.path.exists(target_file_path):
                print(f"⏩ Skipped (already exists): {member.filename}")
                skipped_count += 1
            else:
                zip_ref.extract(member, extract_path)
                print(f"✅ Extracted: {member.filename}")
                extracted_count += 1

print(f"\nFinished processing! Extracted: {extracted_count} | Skipped: {skipped_count}\n")

# 4. Read ALL extracted CSV files into PySpark DataFrame
df_all = (
    spark.read
    .option("header", "true")
    .option("inferSchema", "true")
    .option("recursiveFileLookup", "true")
    .csv("Files/archive_unzipped")
)

print(f"Total rows in dataset: {df_all.count():,}")
display(df_all)
