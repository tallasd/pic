import os
import requests
import re
import time
from compose_image import create_pokemon_card

# Create directories
if not os.path.exists("downloads"):
    os.makedirs("downloads")
if not os.path.exists("output"):
    os.makedirs("output")

raw_list = """
6IV Shiny Armarouge
6IV Latios Shiny
6IV Shiny Tatsugiri
6IV Shiny Milotic
6IV Latias Shiny
6IV Shiny Ceruledge
6IV Shiny Tatsugiri
6IV Shiny Grapploct
6IV Shiny Treecko
6IV Shiny Cofagrigus
6IV Shiny Gholdengo
6IV Shiny Amoonguss
6IV Shiny Torchic
6IV Shiny Virizion
6IV Shiny Cobalion
6IV Shiny Starly
6IV Shiny Mr. Rime
6IV Shiny Glimmet
6IV Shiny Glimmora
6IV Shiny Baxcalibur
6IV Shiny Mudkip
6IV Shiny Cyclizar
6IV Shiny Morpeko
6IV Shiny Kecleon
6IV Shiny Crobat
6IV Shiny Indeedee
6IV Shiny Dondozo
6IV Shiny Runerigus
6IV Shiny Golispod
6IV Shiny Frigibax
6IV Shiny Golett
6IV Shiny Crabrawler
6IV Shiny Sirfetch'd
6IV Shiny Seviper
6IV Shiny Blaziken
6IV Shiny Tatsugiri
6IV Shiny Corviknight
6IV Shiny Feebas
6IV Shiny Thievul
6IV Shiny Rotom
6IV Shiny Farfetch'd Gal
6IV Shiny Wimpod
6IV Shiny Golurk
6IV Shiny Throh
6IV Shiny Annihilape
6IV Shiny Maschiff
6IV Shiny Marowak Alolan
6IV Shiny Charcadet
6IV Shiny Tinkatink
6IV Shiny Zangoose
6IV Shiny Toxel
6IV Shiny Arctibax
6IV Shiny Cubone
6IV Shiny Foongus
6IV Shiny Sawk
6IV Shiny Kleavor
6IV Shiny Chimecho
6IV Shiny Wigglytuff
6IV Shiny Tinkaton
6IV Shiny Houndstone
6IV Shiny Chingling
6IV Shiny Nickit
6IV Shiny Swampert
6IV Shiny Musharna
6IV Shiny Mow Rotom
6IV Shiny Spoink
6IV Shiny Glimmora
6IV Shiny Rookidee
6IV Shiny Mr. Mime
6IV Shiny Staraptor
6IV Shiny Capsakid
6IV Shiny Munna
6IV Shiny Scovillain
6IV Shiny Sandygast
6IV Shiny Terrakion
6IV Shiny Gimmighoul
6IV Shiny Grumpig
6IV Shiny Mimikyu
6IV Shiny Mr. Mime Gala
6IV Shiny Tinkatuff
6IV Shiny Mankey
6IV Shiny Marowak
6IV Shiny Grafaiai
6IV Shiny Farfetch'd
6IV Shiny Squawkabilly
6IV Shiny Nacli
6IV Shiny Persian Alolan
6IV Shiny Qwilfish
6IV Shiny Meowth
6IV Shiny Palossand
6IV Shiny Frost Rotom
6IV Shiny Zumbat
6IV Shiny Shroodle
6IV Shiny Naclstack
6IV Shiny Crabominable
6IV Shiny Golbat
6IV Shiny Greavard
6IV Shiny Igglybuff
6IV Shiny Treecko
6IV Shiny Grovyle
6IV Shiny Combusken
6IV Shiny Yamask
6IV Shiny Sceptile
6IV Shiny Purrloin
6IV Shiny Liepard
6IV Shiny Squawkabilly
6IV Shiny Fidough
6IV Shiny Marshtomp
6IV Shiny Squawkabilly
6IV Shiny Cryogonal
6IV Shiny Squawkabilly
6IV Shiny Overqwil
6IV Shiny Porygon Z
6IV Shiny Clobbopus
6IV Shiny Primeape
6IV Shiny Indeedee Male
6IV Shiny Corvisquire
6IV Shiny Qwilfish Hisui
6IV Shiny Flamigo
6IV Shiny Yamask Gala
6IV Shiny Perrserker
6IV Shiny Wash Rotom
6IV Shiny Mabosstiff
6IV Shiny Garganacl
6IV Shiny Swalot
6IV Shiny Staravia
6IV Shiny Fan Rotom
6IV Shiny Porygon
6IV Shiny Persian
6IV Shiny Gulpin
6IV Shiny Gholdengo
6IV Shiny Heat Rotom
6IV Shiny Meowth Galar
6IV Shiny Meowth Alolan
6IV Shiny Torchic
6IV Shiny Tinkatink
6IV Shiny Toxtricity Amped
6IV Shiny Dachsbun
6IV Shiny Porygon2
6IV Shiny Jigglypuff
6IV Shiny Mime Jr.
6IV Shiny Blaziken
6IV Shiny Frigibax
6IV Shiny Charcadet
6IV Shiny Mudkip
6IV Shiny Toxtricity Low Key
6IV Shiny Crabrawler
6IV Shiny Swampert
6IV Shiny Staraptor
6IV Shiny Milotic
6IV Shiny Zubat
6IV Shiny Tinkaton
6IV Shiny Glimmet
6IV Shiny Starly
6IV Shiny Baxcalibur
6IV Shiny Golurk
6IV Shiny Mimikyu
6IV Shiny Crobat
6IV Shiny Feebas
6IV Shiny Gimmighoul
6IV Shiny Liepard
6IV Shiny Mankey
6IV Shiny Sceptile
6IV Shiny Armarouge
6IV Shiny Wigglytuff
6IV Shiny Male Indeedee
6IV Shiny Yamask Galarian
6IV Shiny Toxtricity
6IV Shiny Mr. Mime Galarian
6IV Shiny Chimecho
6IV Shiny Capsakid
6IV Shiny Arctibax
6IV Shiny Annihilape
6IV Shiny Zangoose
6IV Shiny Nickit
6IV Shiny Ceruledge
6IV Shiny Wimpod
6IV Shiny Mow Rotom
6IV Shiny Tatsugiri
6IV Shiny Rookidee
6IV Shiny Fan Rotom
6IV Shiny Mime Jr
6IV Shiny Porygon 2
6IV Shiny Marowak Alolan
6IV Shiny Crabominable
6IV Shiny Kecleon
6IV Shiny Persian Alola
6IV Shiny Igglybuff
6IV Shiny Combusken
6IV Shiny Toxel
6IV Shiny Cryogonal
6IV Shiny Clobbopus
6IV Shiny Heat Rotom
6IV Shiny Golett
6IV Shiny Cofagrigus
6IV Shiny Scovillain
6IV Shiny Greavard
6IV Shiny Primeape
6IV Shiny Musharna
6IV Shiny Porygon Z
6IV Shiny Female Indeedee
6IV Shiny Thievul
6IV Shiny Frost Rotom
6IV Shiny Cyclizar
6IV Shiny Sawk
6IV Shiny Throh
6IV Shiny Mr Mime
"""

def clean_name(raw):
    # Remove "6IV", "Shiny", "Latios Shiny" -> "Latios"
    name = raw.replace("6IV", "").replace("Shiny", "").strip()
    
    # Fix specific typos and forms from user list
    name_map = {
        "Golispod": "Golisopod",
        "Zumbat": "Zubat",
        "Farfetch'd Gal": "Farfetch'd Galarian",
        "Mr. Mime Gala": "Mr. Mime Galarian",
        "Yamask Gala": "Yamask Galarian",
        "Yamask Galarian": "Yamask Galarian",
        "Persian Alola": "Persian Alolan",
        "Qwilfish Hisui": "Qwilfish Hisuian",
        "Mr Mime": "Mr. Mime",
        "Porygon 2": "Porygon2",
        "Mime Jr": "Mime Jr.",
        "Meowth Galar": "Meowth Galarian",
        "Male Indeedee": "Indeedee Male",
        "Female Indeedee": "Indeedee Female",
        "Indeedee Male": "Indeedee", # Usually male is base form
        "Indeedee Female": "Indeedee Female",
        "Latios": "Latios",
        "Latias": "Latias"
    }
    
    # Check exact matches in map
    if name in name_map:
        name = name_map[name]
        
    return name

def get_slug(name):
    # Convert name to pokemondb slug
    # Lowercase
    slug = name.lower()
    
    # Handle Forms: "Rotom Wash" -> "rotom-wash", "Marowak Alolan" -> "marowak-alolan"
    # User input is typically "Pokemon Form". Pokemondb uses "pokemon-form" usually.
    # But for Rotom it is "rotom-wash", user input is "Wash Rotom".
    # Let's handle specific "Prefix Pokemon" cases.
    
    rotom_forms = ["wash", "mow", "heat", "fan", "frost"]
    for form in rotom_forms:
        if f"{form} rotom" in slug:
            return f"rotom-{form}"
            
    # Handle "Alolan", "Galarian", "Hisuian", "Paldean" suffixes
    # "Marowak Alolan" -> "marowak-alolan" (Standard)
    # "Farfetch'd Galarian" -> "farfetchd-galarian"
    
    # Replace special chars
    slug = slug.replace(". ", "-") # Mr. Mime -> mr-mime
    slug = slug.replace(".", "")   # Mr.Rime -> MrRime (if any)
    slug = slug.replace("'", "")   # Farfetch'd -> farfetchd
    slug = slug.replace(" ", "-")
    slug = slug.replace("♀", "-f")
    slug = slug.replace("♂", "-m")
    
    return slug

def download_image(name, slug):
    # Try to find ID from PokeAPI
    try:
        # 1. Get ID
        api_url = f"https://pokeapi.co/api/v2/pokemon/{slug}"
        print(f"Fetching ID for {name} ({slug})...")
        r = requests.get(api_url, timeout=10)
        
        if r.status_code == 200:
            data = r.json()
            pokemon_id = data['id']
            
            # 2. Construct Official Artwork URL (Transparent PNG)
            # Standard Official Art
            img_url = f"https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/other/official-artwork/{pokemon_id}.png"
            
            # Alternative: Pokemon Home render (also high quality transparent)
            # img_url = f"https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/other/home/{pokemon_id}.png"
            
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

    # Fallback to old method (pokemondb) if API fails, but user prefers the "official" look
    # Let's try pokemondb vector art if possible? Or keep the old fallback but warn.
    # Actually, let's try the assets.pokemon.com URL with ID if we found ID?
    # But assets.pokemon.com needs 3-digit ID (e.g. 001).
    
    return None

def process_batch():
    lines = raw_list.strip().split('\n')
    bg_file = "Gemini_Generated_Image_5lr6yq5lr6yq5lr6.png"
    
    processed_count = 0
    unique_names = set()
    
    for line in lines:
        if not line.strip():
            continue
            
        clean = clean_name(line)
        
        # Deduplicate based on cleaned name
        if clean in unique_names:
            print(f"Skipping duplicate: {clean}")
            continue
        unique_names.add(clean)
        
        slug = get_slug(clean)
        print(f"Processing: {clean} -> {slug}")
        
        img_path = download_image(clean, slug)
        
        if img_path:
            # Output filename
            safe_name = clean.replace(" ", "_").replace("'", "").replace(".", "")
            out_file = f"output/output_{safe_name}.png"
            
            try:
                # Call the composition function
                # Note: The original name is passed for text rendering (e.g. "MR. MIME")
                create_pokemon_card(bg_file, img_path, clean.upper(), out_file)
                processed_count += 1
            except Exception as e:
                print(f"Error generating card for {clean}: {e}")
        else:
            print(f"Skipping generation for {clean} due to missing image.")
            
        # Be nice to the server
        time.sleep(0.5)

if __name__ == "__main__":
    process_batch()
