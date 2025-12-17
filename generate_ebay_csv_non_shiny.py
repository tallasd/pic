import csv
import os
import requests
import re
import urllib.parse
from concurrent.futures import ThreadPoolExecutor

# File paths
input_list = r"d:\chromedownload\批量产图\pokemon_list.txt"
csv_db = r"d:\chromedownload\批量产图\全部宝可梦数据excel含dlc.csv"
target_csv = r"d:\chromedownload\批量产图\ebay_upload_non_shiny.csv"

# Base URLs
# Use the non-shiny folder for images
GITHUB_BASE_URL = "https://raw.githubusercontent.com/tallasd/pic/main/output_non_shiny/"
SECONDARY_IMAGE_URL = "https://raw.githubusercontent.com/tallasd/pic/main/Gemini_Generated_Image_5sh1k65sh1k65sh1.png"

# Headers (Same as before)
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

# Static values
STATIC_VALUES = {
    "*Action(SiteID=US|Country=US|Currency=USD|Version=1193|CC=UTF-8)": "Add",
    "*Category": "139973", # Video Games
    "*ConditionID": "1000", # Brand New
    "*C:Game Name": "Pokémon Legends: Z-A",
    "*C:Platform": "Nintendo Switch",
    "*Format": "FixedPrice",
    "*Duration": "GTC",
    "*StartPrice": "2.00",
    "*Quantity": "10",
    "*Location": "United States",
    "ShippingType": "Flat",
    "ShippingService-1:Option": "USPSFirstClass",
    "ShippingService-1:Cost": "0",
    "*DispatchTimeMax": "3",
    "*ReturnsAcceptedOption": "ReturnsNotAccepted"
}

def load_non_shiny_list():
    lines = []
    found_section = False
    try:
        with open(input_list, 'r', encoding='utf-8') as f:
            for line in f:
                line = line.strip()
                if "【普通宝可梦 (Non-Shiny)】" in line:
                    found_section = True
                    continue
                if found_section and line:
                    if "【" in line: 
                        break
                    lines.append(line)
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
    
    # Capitalize for Title
    en_name_title = en_name.title()
    en_name_upper = en_name.upper()
    
    print(f"Processed: {cn_name} -> {en_name_title}")
    
    # Construct row
    row = {}
    
    # SKU: ZA_6IV_NON_SHINY_NAME_UPPER
    # Differentiating from shiny SKU
    sku_name = en_name_upper.replace(" ", "_").replace(".", "").replace("'", "")
    row["CustomLabel"] = f"ZA_6IV_NON_SHINY_{sku_name}"
    
    # Title: 6IV [Name] Legends ZA MEGA DIMENSION DLC (Legends Z-A) - CUSTOM OT
    # Removed "Non-Shiny" as per user request
    row["*Title"] = f"6IV {en_name_title} Legends ZA MEGA DIMENSION DLC (Legends Z-A) - CUSTOM OT"
    
    # PicURL: output_non_shiny/ENGLISH_NAME.png
    # My batch generation script saved files as UPPERCASE ENGLISH NAME.png
    # e.g. ABRA.png
    # Need to make sure URL matches that.
    img_filename = f"{en_name_upper}.png"
    # Although generated script used uppercase, URL is case sensitive on GitHub?
    # Actually, GitHub URLs are case sensitive. My script saved as UPPERCASE.
    # So I should use UPPERCASE.
    
    img_url = f"{GITHUB_BASE_URL}{img_filename}"
    row["PicURL"] = f"{img_url}|{SECONDARY_IMAGE_URL}"
    
    # Description (Updated to remove Shiny/Non-Shiny references)
    # Match reference format: <h1>{Name} 6IV + FREE MASTERBALL GIFT</h1>
    desc = f"""<h1>{en_name_upper} 6IV + FREE MASTERBALL GIFT</h1><p>Ensure to message me here on eBay your set preferences and your hours of availability so we can arrange the trade session!</p><h3>Before You Buy</h3><ul><li>You must have access to Nintendo Online Subscription</li></ul><h3>Contact information</h3><p>Please contact me via eBay messages or through discord: <strong>takemidelivery</strong></p><h3>How to trade in Pokémon Legends: Z-A</h3><ol><li>Go in-game, Press X, Select <strong>Link Play</strong></li><li>Select <strong>Link Trade</strong>, Select <strong>Faraway Players</strong></li><li>Enter the code we will provide.</li><li>Press &quot;+&quot; and select &quot;Begin Searching&quot;.</li><li>Trade me any pokémon and I will trade you what you have purchased!</li></ol><p><strong>Note:</strong> You are purchasing a digital product in the Pokémon Legends: Z-A game. Nothing physical will be delivered to you! Please understand this before purchasing.</p><hr><p>✅ 100% Legit for Battle &amp; Trade<br>✅ Customizable Moves, Nature, Ball, and More<br>✅ Fast &amp; Secure</p>"""
    row["*Description"] = desc
    
    # Fill static values
    for k, v in STATIC_VALUES.items():
        row[k] = v
        
    return row

def main():
    print("Loading non-shiny data...")
    pkmn_list = load_non_shiny_list()
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
            # Write metadata header first
            f.write("Info,Version=1.0.0,Template=fx_category_template_EBAY_US,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,\n")
            
            # Write content
            writer = csv.DictWriter(f, fieldnames=HEADERS)
            writer.writeheader()
            writer.writerows(results)
        print(f"Successfully wrote to {target_csv}")
    except Exception as e:
        print(f"Error writing CSV: {e}")

if __name__ == "__main__":
    main()
