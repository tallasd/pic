import os
import requests
from compose_image import create_pokemon_card
import time

# List of missing items with their corrected API slugs and display names
missing_items = [
    {"name": "Farfetch'd Galarian", "slug": "farfetchd-galar", "file_name": "output_Farfetchd_Galarian.png"},
    {"name": "Indeedee", "slug": "indeedee-male", "file_name": "output_Indeedee.png"}, # Assuming base Indeedee is Male
    {"name": "Marowak Alolan", "slug": "marowak-alola", "file_name": "output_Marowak_Alolan.png"},
    {"name": "Meowth Alolan", "slug": "meowth-alola", "file_name": "output_Meowth_Alolan.png"},
    {"name": "Mimikyu", "slug": "mimikyu-disguised", "file_name": "output_Mimikyu.png"},
    {"name": "Mr. Mime Galarian", "slug": "mr-mime-galar", "file_name": "output_Mr_Mime_Galarian.png"},
    {"name": "Persian Alolan", "slug": "persian-alola", "file_name": "output_Persian_Alolan.png"},
    {"name": "Qwilfish Hisuian", "slug": "qwilfish-hisui", "file_name": "output_Qwilfish_Hisuian.png"},
    {"name": "Squawkabilly", "slug": "squawkabilly-green-plumage", "file_name": "output_Squawkabilly.png"},
    {"name": "Tatsugiri", "slug": "tatsugiri-curly", "file_name": "output_Tatsugiri.png"}, # Curly form is default/common? Or just pick one.
    {"name": "Yamask Galarian", "slug": "yamask-galar", "file_name": "output_Yamask_Galarian.png"}
]

def download_image_by_slug(name, slug):
    try:
        # 1. Get ID
        api_url = f"https://pokeapi.co/api/v2/pokemon/{slug}"
        print(f"Fetching ID for {name} ({slug})...")
        r = requests.get(api_url, timeout=10)
        
        if r.status_code == 200:
            data = r.json()
            pokemon_id = data['id']
            
            # 2. Construct Official Artwork URL (Transparent PNG)
            img_url = f"https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/other/official-artwork/{pokemon_id}.png"
            
            filename = f"downloads/{slug}.png"
            
            print(f"Downloading {name} from {img_url}...")
            img_r = requests.get(img_url, timeout=10)
            
            if img_r.status_code == 200:
                with open(filename, 'wb') as f:
                    f.write(img_r.content)
                print(f"Downloaded: {filename}")
                return filename
            else:
                print(f"Image not found at {img_url}")
        else:
            print(f"Pokemon not found in API: {slug}")
            
    except Exception as e:
        print(f"Error downloading {name}: {e}")
    return None

def process_missing():
    bg_file = "Gemini_Generated_Image_5lr6yq5lr6yq5lr6.png"
    
    for item in missing_items:
        name = item["name"]
        slug = item["slug"]
        out_file = f"output/{item['file_name']}"
        
        print(f"Processing missing: {name} -> {slug}")
        
        img_path = download_image_by_slug(name, slug)
        
        if img_path:
            try:
                # Use the clean name for display (uppercase)
                display_name = name.replace("6IV", "").replace("Shiny", "").strip().upper()
                create_pokemon_card(bg_file, img_path, display_name, out_file)
                print(f"Saved to {out_file}")
            except Exception as e:
                print(f"Error generating card for {name}: {e}")
        else:
            print(f"Failed to get image for {name}")
            
        time.sleep(0.5)

if __name__ == "__main__":
    process_missing()
