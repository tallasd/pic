import csv
import os
from batch_process import raw_list, clean_name

# Configuration
TEMPLATE_FILE = r"d:\chromedownload\批量产图\eBay-category-listing-template-12月-15-2025-9-22-35.csv"
OUTPUT_CSV = r"d:\chromedownload\批量产图\ebay_listings_generated.csv"
SECOND_IMAGE_PATH_LOCAL = r"D:\chromedownload\批量产图\Gemini_Generated_Image_5sh1k65sh1k65sh1.png"
OUTPUT_DIR = r"D:\chromedownload\批量产图\output"

# GitHub Configuration (Replace with your actual details)
GITHUB_USER = "YOUR_USERNAME"
GITHUB_REPO = "YOUR_REPO_NAME"
GITHUB_BRANCH = "main"
# Base URL for raw images
GITHUB_BASE_URL = f"https://raw.githubusercontent.com/{GITHUB_USER}/{GITHUB_REPO}/{GITHUB_BRANCH}"

def get_safe_name(name):
    return name.replace(" ", "_").replace("'", "").replace(".", "")

def generate_csv():
    # Read the header from the template
    with open(TEMPLATE_FILE, 'r', encoding='utf-8') as f:
        lines = f.readlines()
        
    # eBay CSVs often have comments/metadata in the first few lines
    # The header line usually starts with *Action or Action
    header_line_index = -1
    for i, line in enumerate(lines):
        if "Action" in line:
            header_line_index = i
            break
            
    if header_line_index == -1:
        print("Error: Could not find header line in template.")
        return

    # Keep the metadata lines
    metadata_lines = lines[:header_line_index]
    header = lines[header_line_index].strip().split(',')
    
    # Process the pokemon list
    pokemon_lines = raw_list.strip().split('\n')
    rows = []
    
    unique_names = set()

    for line in pokemon_lines:
        if not line.strip():
            continue
            
        name = clean_name(line)
        
        # Deduplicate
        if name in unique_names:
            continue
        unique_names.add(name)
        
        safe_name = get_safe_name(name)
        image_name = f"output_{safe_name}.png"
        # image_path = os.path.join(OUTPUT_DIR, image_name) # Local path - not used for CSV
        
        # Construct GitHub URLs
        # URL for the Pokemon image
        pic_url_1 = f"{GITHUB_BASE_URL}/output/{image_name}"
        # URL for the background/second image (assuming it's in the root of the repo)
        pic_url_2 = f"{GITHUB_BASE_URL}/Gemini_Generated_Image_5sh1k65sh1k65sh1.png"
        
        # Title
        title = f"6IV Shiny {name} Legends ZA MEGA DIMENSION DLC (Legends Z-A) - CUSTOM OT"
        
        # Description
        description = f"""<h1>SHINY {name.upper()} 6IV + FREE MASTERBALL GIFT</h1>
<p>Purchasing the DLC is not required; trades can also be made with players who do not own it.</p>
<p><strong>How to trade in Pokémon Legends Z-A:</strong></p>
<p>Press "+" and select "Begin Searching".</p>"""

        # Images (pipe separated)
        pic_url = f"{pic_url_1}|{pic_url_2}"
        
        # Map to CSV columns
        row = {}
        for col in header:
            row[col] = "" # Default empty
            
        # Fill required/standard fields
        # Let's handle the Action key specifically because it's long
        action_key = [k for k in header if "Action" in k][0]
        
        row[action_key] = "Add"
        row['*Category'] = "139973" # Video Games
        row['*Title'] = title
        row['*ConditionID'] = "1000" # Brand New
        row['*C:Game Name'] = "Pokémon Legends: Z-A"
        row['*C:Platform'] = "Nintendo Switch"
        row['*Description'] = description
        row['*Format'] = "FixedPrice"
        row['*Duration'] = "GTC"
        row['*StartPrice'] = "4.49" # Based on screenshot
        row['*Quantity'] = "10"
        row['*Location'] = "China" 
        row['*DispatchTimeMax'] = "3"
        row['*ReturnsAcceptedOption'] = "ReturnsNotAccepted"
        row['PicURL'] = pic_url
        
        # Shipping Details
        row['ShippingType'] = "Flat"
        row['ShippingService-1:Option'] = "StandardInternational" # Common for China -> US
        row['ShippingService-1:Cost'] = "0" # Free shipping
        
        # Ordered values
        row_values = [row.get(col, "") for col in header]
        rows.append(row_values)

    # Write output
    with open(OUTPUT_CSV, 'w', encoding='utf-8', newline='') as f:
        # Write metadata
        for line in metadata_lines:
            f.write(line)
            
        writer = csv.writer(f)
        writer.writerow(header)
        writer.writerows(rows)
        
    print(f"Generated CSV with {len(rows)} listings at {OUTPUT_CSV}")

if __name__ == "__main__":
    generate_csv()
