from compose_image import create_pokemon_card
import os

# Configuration
bg_file = "2kChatGPT Image 2025年12月17日 14_56_29.jpg"
pokemon_name = "Amoonguss"
pokemon_file = "downloads/amoonguss.png"
output_file = "sample_output.png"

# Verify files exist
if not os.path.exists(bg_file):
    print(f"Error: Background file not found: {bg_file}")
    exit(1)

if not os.path.exists(pokemon_file):
    print(f"Error: Pokemon file not found: {pokemon_file}")
    # Try to find any png in downloads
    files = [f for f in os.listdir("downloads") if f.endswith(".png")]
    if files:
        pokemon_file = os.path.join("downloads", files[0])
        print(f"Using alternative pokemon file: {pokemon_file}")
    else:
        print("No pokemon images found in downloads/")
        exit(1)

print(f"Generating sample image using background: {bg_file}")
create_pokemon_card(bg_file, pokemon_file, pokemon_name, output_file)

if os.path.exists(output_file):
    print(f"Success! Sample image generated at: {os.path.abspath(output_file)}")
else:
    print("Error: Failed to generate sample image.")
