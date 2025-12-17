import os
import re

output_dir = r"d:\chromedownload\批量产图\output"

def contains_chinese(text):
    return bool(re.search(r'[\u4e00-\u9fa5]', text))

deleted_count = 0
print(f"Scanning {output_dir}...")

if not os.path.exists(output_dir):
    print("Output directory does not exist.")
    exit()

for filename in os.listdir(output_dir):
    if not filename.endswith(".png"):
        continue
        
    # Check if filename contains Chinese
    # If it DOES NOT contain Chinese, delete it (it's an old English file)
    if not contains_chinese(filename):
        file_path = os.path.join(output_dir, filename)
        try:
            os.remove(file_path)
            # print(f"Deleted: {filename}") # Comment out to avoid spamming output if many files
            deleted_count += 1
        except Exception as e:
            print(f"Error deleting {filename}: {e}")

print(f"Total deleted: {deleted_count}")
