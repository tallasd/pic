import csv
import os
import requests
import re
import urllib.parse
from concurrent.futures import ThreadPoolExecutor

# File paths
input_list = r"d:\chromedownload\批量产图\pokemon_list.txt"
csv_db = r"d:\chromedownload\批量产图\全部宝可梦数据excel含dlc.csv"
target_csv = r"d:\chromedownload\批量产图\只有这个可以用ebay_upload_ready_legends_za_flat_with_sku.csv"
output_dir = r"d:\chromedownload\批量产图\output"

# Base URLs
GITHUB_BASE_URL = "https://raw.githubusercontent.com/tallasd/pic/main/output/"
SECONDARY_IMAGE_URL = "https://raw.githubusercontent.com/tallasd/pic/main/Gemini_Generated_Image_5sh1k65sh1k65sh1.png"

# Headers from the target CSV
HEADERS = [
    "*Action(SiteID=US|Country=US|Currency=USD|Version=1193|CC=UTF-8)", "CustomLabel", "*Category", "StoreCategory", "*Title", "Subtitle",
    "Relationship", "RelationshipDetails", "ScheduleTime", "*ConditionID", "*C:Game Name", "*C:Platform", "C:Publisher", "C:Genre",
    "C:Rating", "C:Region Code", "C:Release Year", "C:MPN", "C:Unit Quantity", "C:Unit Type", "C:Video Game Series", "C:Features",
    "C:Country of Origin", "C:Sub-Genre", "C:California Prop 65 Warning", "C:Manufacturer Warranty", "PicURL", "GalleryType", "VideoID",
    "*Description", "*Format", "*Duration", "*StartPrice", "BuyItNowPrice", "BestOfferEnabled", "BestOfferAutoAcceptPrice",
    "MinimumBestOfferPrice", "*Quantity", "ImmediatePayRequired", "*Location", "ShippingType", "ShippingService-1:Option",
    "ShippingService-1:Cost", "ShippingService-2:Option", "ShippingService-2:Cost", "*DispatchTimeMax", "PromotionalShippingDiscount",
    "ShippingDiscountProfileID", "*ReturnsAcceptedOption", "ReturnsWithinOption", "RefundOption", "ShippingCostPaidByOption",
    "AdditionalDetails", "Product Safety Pictograms", "Product Safety Statements", "Product Safety Component", "Regulatory Document Ids",
    "Manufacturer Name", "Manufacturer AddressLine1", "Manufacturer AddressLine2", "Manufacturer City", "Manufacturer Country",
    "Manufacturer PostalCode", "Manufacturer StateOrProvince", "Manufacturer Phone", "Manufacturer Email", "Manufacturer ContactURL",
    "Responsible Person 1", "Responsible Person 1 Type", "Responsible Person 1 AddressLine1", "Responsible Person 1 AddressLine2",
    "Responsible Person 1 City", "Responsible Person 1 Country", "Responsible Person 1 PostalCode", "Responsible Person 1 StateOrProvince",
    "Responsible Person 1 Phone", "Responsible Person 1 Email", "Responsible Person 1 ContactURL"
]

# Static values for new rows
STATIC_VALUES = {
    "*Action(SiteID=US|Country=US|Currency=USD|Version=1193|CC=UTF-8)": "Add",
    "*Category": "139973", # Video Games
    "*ConditionID": "1000", # Brand New
    "*C:Game Name": "Pokémon Legends: Z-A",
    "*C:Platform": "Nintendo Switch",
    "*Format": "FixedPrice",
    "*Duration": "GTC",
    "*StartPrice": "4.49",
    "*Quantity": "10",
    "*Location": "United States",
    "ShippingType": "Flat",
    "ShippingService-1:Option": "USPSFirstClass",
    "ShippingService-1:Cost": "0",
    "*DispatchTimeMax": "3",
    "*ReturnsAcceptedOption": "ReturnsNotAccepted"
}

def load_pokemon_list():
    lines = []
    try:
        with open(input_list, 'r', encoding='utf-8') as f:
            content = f.read()
            if "【闪光宝可梦 (Shiny)】" in content:
                shiny_part = content.split("【闪光宝可梦 (Shiny)】")[1]
                if "【普通宝可梦 (Non-Shiny)】" in shiny_part:
                    shiny_part = shiny_part.split("【普通宝可梦 (Non-Shiny)】")[0]
                lines = [l.replace("★", "").strip() for l in shiny_part.strip().split('\n') if l.strip()]
    except Exception as e:
        print(f"Error reading list: {e}")
    return lines

def load_id_map():
    name_to_id = {}
    try:
        with open(csv_db, 'r', encoding='utf-8') as f:
            reader = csv.reader(f)
            headers = next(reader)
            species_idx = headers.index("Species")
            position_idx = headers.index("Position")
            
            for row in reader:
                if not row: continue
                name = row[species_idx]
                pos_str = row[position_idx]
                match = re.search(r':\s*(\d+)', pos_str)
                if match:
                    dex_id = int(match.group(1))
                    name_to_id[name] = dex_id
    except Exception as e:
        print(f"Error loading ID map: {e}")
    return name_to_id

def get_english_name(dex_id):
    url = f"https://pokeapi.co/api/v2/pokemon-species/{dex_id}"
    try:
        r = requests.get(url, timeout=10)
        if r.status_code == 200:
            data = r.json()
            for entry in data['names']:
                if entry['language']['name'] == 'en':
                    return entry['name']
    except Exception as e:
        print(f"Error fetching English name for ID {dex_id}: {e}")
    return None

def process_item(cn_name, dex_id):
    en_name = get_english_name(dex_id)
    if not en_name:
        print(f"Could not find English name for {cn_name} (ID: {dex_id})")
        return None
    
    print(f"Processed: {cn_name} -> {en_name}")
    
    # Construct row
    row = {}
    
    # SKU: ZA_6IV_SHINY_NAME_UPPER
    sku_name = en_name.upper().replace(" ", "_").replace(".", "").replace("'", "")
    row["CustomLabel"] = f"ZA_6IV_SHINY_{sku_name}"
    
    # Title: 6IV Shiny Name ...
    row["*Title"] = f"6IV Shiny {en_name} Legends ZA MEGA DIMENSION DLC (Legends Z-A) - CUSTOM OT"
    
    # PicURL: output_ChineseName.png (URL Encoded)
    # Filename on disk is output_中文.png
    safe_cn_name = urllib.parse.quote(cn_name)
    img_url = f"{GITHUB_BASE_URL}output_{safe_cn_name}.png"
    row["PicURL"] = f"{img_url}|{SECONDARY_IMAGE_URL}"
    
    # Description
    desc = f"""<h1>SHINY {en_name.upper()} 6IV + FREE MASTERBALL GIFT</h1><p>Purchasing the DLC is not required; trades can also be made with players who do not own it.</p><p><strong>How to trade in Pokémon Legends Z-A:</strong></p><p>Press ""+"" and select ""Begin Searching"".</p>"""
    row["*Description"] = desc
    
    # Fill static values
    for k, v in STATIC_VALUES.items():
        row[k] = v
        
    return row

def main():
    print("Loading data...")
    pkmn_list = load_pokemon_list()
    id_map = load_id_map()
    
    print(f"Found {len(pkmn_list)} items to process.")
    
    results = []
    
    # Use ThreadPool to speed up API calls
    with ThreadPoolExecutor(max_workers=10) as executor:
        futures = []
        for cn_name in pkmn_list:
            dex_id = id_map.get(cn_name)
            if dex_id:
                futures.append(executor.submit(process_item, cn_name, dex_id))
            else:
                print(f"Warning: No ID found for {cn_name}")
        
        for f in futures:
            res = f.result()
            if res:
                results.append(res)
                
    print(f"Generated {len(results)} rows.")
    
    # Write CSV
    try:
        with open(target_csv, 'w', encoding='utf-8', newline='') as f:
            writer = csv.DictWriter(f, fieldnames=HEADERS)
            writer.writeheader()
            writer.writerows(results)
        print(f"Successfully wrote to {target_csv}")
    except Exception as e:
        print(f"Error writing CSV: {e}")

if __name__ == "__main__":
    main()
