import os
import sys
from compose_image import create_pokemon_card

# Target background (New JPG)
bg_path = r"d:\chromedownload\批量产图\ChatGPT Image 2025年12月18日 00_51_48.jpg"

# Target Pokemon (Abra, ID 63)
pokemon_path = r"d:\chromedownload\批量产图\downloads\63.png"
pokemon_name = "ABRA"

# Output
output_path = r"d:\chromedownload\批量产图\sample_non_shiny_abra_v2.png"

if not os.path.exists(bg_path):
    print(f"Error: Background not found at {bg_path}")
    sys.exit(1)

if not os.path.exists(pokemon_path):
    print(f"Error: Pokemon image not found at {pokemon_path}")
    sys.exit(1)

print(f"Generating sample with background: {bg_path}")
print(f"Pokemon: {pokemon_name} ({pokemon_path})")

try:
    create_pokemon_card(bg_path, pokemon_path, pokemon_name, output_path)
    print(f"Success! Output saved to: {output_path}")
except Exception as e:
    print(f"Failed to generate image: {e}")
