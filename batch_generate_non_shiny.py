import csv
import os
import requests
import re
import sys
from concurrent.futures import ThreadPoolExecutor
from compose_image import create_pokemon_card

# Paths
LIST_FILE = r"d:\chromedownload\批量产图\pokemon_list.txt"
CSV_DB = r"d:\chromedownload\批量产图\全部宝可梦数据excel含dlc.csv"
BG_PATH = r"d:\chromedownload\批量产图\ChatGPT Image 2025年12月18日 00_51_48.jpg"
DOWNLOADS_DIR = r"d:\chromedownload\批量产图\downloads"
OUTPUT_DIR = r"d:\chromedownload\批量产图\output_non_shiny"

# Ensure output dir exists
os.makedirs(OUTPUT_DIR, exist_ok=True)

def load_non_shiny_names():
    names = []
    found_section = False
    try:
        with open(LIST_FILE, 'r', encoding='utf-8') as f:
            for line in f:
                line = line.strip()
                if "【普通宝可梦 (Non-Shiny)】" in line:
                    found_section = True
                    continue
                if found_section and line:
                    if "【" in line: 
                        break
                    names.append(line)
    except Exception as e:
        print(f"Error reading list file: {e}")
    return names

def load_id_map():
    name_to_id = {}
    try:
        with open(CSV_DB, 'r', encoding='utf-8') as f:
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
                    name_to_id[name] = int(match.group(1))
    except Exception as e:
        print(f"Error loading ID map: {e}")
    return name_to_id

def get_english_name(dex_id):
    # Try API
    url = f"https://pokeapi.co/api/v2/pokemon-species/{dex_id}"
    try:
        r = requests.get(url, timeout=10)
        if r.status_code == 200:
            data = r.json()
            for entry in data['names']:
                if entry['language']['name'] == 'en':
                    return entry['name'].upper()
    except Exception as e:
        print(f"Error fetching English name for ID {dex_id}: {e}")
    return f"POKEMON_{dex_id}" 

def process_pokemon(name, dex_id):
    # Get English name first (needed for filename search)
    english_name = get_english_name(dex_id)
    print(f"Processing {name} -> {english_name} (ID: {dex_id})...")

    # 1. Find image (ID first, then English name)
    img_path = None
    
    # Check ID-based names
    candidates = [
        f"{dex_id}.png",
        f"{dex_id}.jpg",
        f"{english_name}.png",
        f"{english_name}.jpg",
        f"{english_name.lower()}.png",
        f"{english_name.lower()}.jpg"
    ]
    
    for cand in candidates:
        p = os.path.join(DOWNLOADS_DIR, cand)
        if os.path.exists(p):
            img_path = p
            break
            
    if not img_path:
        print(f"Image not found locally for {name} (ID: {dex_id}). Attempting download...")
        try:
            download_url = f"https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/other/official-artwork/{dex_id}.png"
            dl_path = os.path.join(DOWNLOADS_DIR, f"{dex_id}.png")
            r = requests.get(download_url, timeout=10)
            if r.status_code == 200:
                with open(dl_path, 'wb') as f:
                    f.write(r.content)
                print(f"Downloaded {dex_id}.png")
                img_path = dl_path
            else:
                print(f"Failed to download image from {download_url}")
        except Exception as e:
            print(f"Download error: {e}")

    if not img_path:
        print(f"Image not found for {name} (ID: {dex_id}, Name: {english_name}) - Skipping generation")
        return

    # 3. Generate
    output_filename = f"{english_name}.png"
    output_path = os.path.join(OUTPUT_DIR, output_filename)
    
    try:
        create_pokemon_card(BG_PATH, img_path, english_name, output_path)
    except Exception as e:
        print(f"Failed to generate {name}: {e}")

def main():
    print("Starting batch generation for non-shiny pokemon...")
    names = load_non_shiny_names()
    id_map = load_id_map()
    
    print(f"Found {len(names)} non-shiny names in list.")
    
    # Filter only those we have names for
    tasks = []
    # Use max_workers=5 to avoid hitting API limits too hard
    with ThreadPoolExecutor(max_workers=5) as executor:
        for name in names:
            if name in id_map:
                dex_id = id_map[name]
                tasks.append(executor.submit(process_pokemon, name, dex_id))
            else:
                print(f"ID not found for {name}")
                
    print("Batch generation completed.")

if __name__ == "__main__":
    main()
