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
print(f"Found {len(zip_files)} ZIP archive(s) to process.\n")

total_extracted_count = 0

# 3. Loop through each ZIP file and extract ALL inner files
for zip_name in zip_files:
    zip_file_path = os.path.join(archive_dir, zip_name)
    
    with zipfile.ZipFile(zip_file_path, 'r') as zip_ref:
        inner_files = zip_ref.namelist()
        print(f"📦 Unpacking '{zip_name}' — contains {len(inner_files)} file(s):")
        for f in inner_files:
            print(f"   └── {f}")
            
        zip_ref.extractall(extract_path)
        total_extracted_count += len(inner_files)

print(f"\n Extracted {total_extracted_count} total file(s) into: {extract_path}\n")

# 4. Read ALL extracted CSV files into a single consolidated DataFrame
# 'recursiveFileLookup' ensures files inside subfolders (if any existed in the zip) are also read
df_all = (
    spark.read
    .option("header", "true")
    .option("inferSchema", "true")
    .option("recursiveFileLookup", "true")
    .csv("Files/archive_unzipped")
)

print(f" Total rows across all unzipped files: {df_all.count():,}")
display(df_all)


