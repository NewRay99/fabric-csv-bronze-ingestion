import zipfile
import os

# 1. Define paths
base_dir = "/lakehouse/default/Files"

# Automatically find the shortcut folder
shortcut_folder = [f for f in os.listdir(base_dir) if f.startswith("wmpp-production")][0]
archive_dir = os.path.join(base_dir, shortcut_folder, "archive")
extract_base_path = os.path.join(base_dir, "archive_unzipped")

os.makedirs(extract_base_path, exist_ok=True)

# 2. Find all ZIP files
zip_files = [f for f in os.listdir(archive_dir) if f.endswith('.zip')]
print(f"Found {len(zip_files)} ZIP archive(s) to check.\n")

extracted_count = 0
skipped_count = 0

# 3. Loop through each ZIP file
for zip_name in zip_files:
    # Remove .zip extension to get the folder name (e.g., '2026-07-01')
    folder_name = os.path.splitext(zip_name)[0]
    target_folder_path = os.path.join(extract_base_path, folder_name)
    
    # Check if the target folder exists and is non-empty
    if os.path.exists(target_folder_path) and os.listdir(target_folder_path):
        print(f"⏩ Skipped (folder already exists): {folder_name}/")
        skipped_count += 1
    else:
        # Create the specific folder for this zip file
        os.makedirs(target_folder_path, exist_ok=True)
        zip_file_path = os.path.join(archive_dir, zip_name)
        
        # Extract files straight into the date folder
        with zipfile.ZipFile(zip_file_path, 'r') as zip_ref:
            zip_ref.extractall(target_folder_path)
            
        print(f"✅ Extracted: {zip_name} ➔ {folder_name}/")
        extracted_count += 1

print(f"\nFinished processing! Extracted: {extracted_count} | Skipped: {skipped_count}\n")

# 4. Read ALL CSV files across all date subfolders into PySpark
df_all = (
    spark.read
    .option("header", "true")
    .option("inferSchema", "true")
    .option("recursiveFileLookup", "true") # Digs into subfolders (2026-07-01/, 2026-07-02/, etc.)
    .csv("Files/archive_unzipped")
)

print(f"Total rows in consolidated dataset: {df_all.count():,}")
display(df_all)
