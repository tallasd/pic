import sys
from PIL import Image, ImageDraw, ImageFont

def make_transparent(img):
    img = img.convert("RGBA")
    # Get the color of the top-left pixel
    # Assume background is white-ish
    # Use floodfill to make it transparent
    # thresh=50 to handle JPG artifacts (0-255 scale)
    try:
        ImageDraw.floodfill(img, (0, 0), (0, 0, 0, 0), thresh=50)
        # Try other corners if they are still white (sometimes corners are isolated)
        w, h = img.size
        # Check and fill other corners if needed
        # Top-Right
        if img.getpixel((w-1, 0))[3] != 0:
             ImageDraw.floodfill(img, (w-1, 0), (0, 0, 0, 0), thresh=50)
        # Bottom-Left
        if img.getpixel((0, h-1))[3] != 0:
             ImageDraw.floodfill(img, (0, h-1), (0, 0, 0, 0), thresh=50)
        # Bottom-Right
        if img.getpixel((w-1, h-1))[3] != 0:
             ImageDraw.floodfill(img, (w-1, h-1), (0, 0, 0, 0), thresh=50)
    except Exception as e:
        print(f"Warning: Failed to remove background: {e}")
    return img

def create_pokemon_card(bg_path, pokemon_path, pokemon_name, output_path):
    # Load images
    try:
        bg = Image.open(bg_path).convert("RGBA")
        pokemon = Image.open(pokemon_path).convert("RGBA")
        
        # Remove background if it looks like a JPG/non-transparent image
        # We apply this to all images to be safe, or we could check if it has transparency
        # But even PNGs might have white bg.
        pokemon = make_transparent(pokemon)
        
        # Crop transparent borders (trim)
        bbox = pokemon.getbbox()
        if bbox:
            pokemon = pokemon.crop(bbox)

    except Exception as e:
        print(f"Error loading images: {e}")
        return

    # Resize pokemon
    # Define Safe Zone for 2048x2048
    # Top Text Area (Custom text + SHINY 6IV): roughly 0-600
    # Bottom Logos Area: roughly 1500-2048
    # Safe area for Pokemon: y=700 to y=1750 (Height = 1050)
    # Max Width: 1800 (Background is 2048, leave some margin)
    
    bg_w, bg_h = bg.size
    
    max_w = 1800
    max_h = 1200
    
    # Calculate resize ratio to fit within max_w and max_h while preserving aspect ratio
    src_w, src_h = pokemon.size
    ratio = min(max_w / src_w, max_h / src_h)
    
    target_w = int(src_w * ratio)
    target_h = int(src_h * ratio)
    
    pokemon_resized = pokemon.resize((target_w, target_h), Image.Resampling.LANCZOS)
    
    # Position: Center horizontally
    pos_x = (bg_w - target_w) // 2
    
    # Position Vertically: Start at y=600 + centering offset (Moved up from 700, down from 500)
    safe_top = 600
    safe_bottom = 1650 # Shifted down by 100
    available_h = safe_bottom - safe_top
    
    # Center in the safe vertical band
    pos_y = safe_top + (available_h - target_h) // 2
    
    # Composite
    # We use the pokemon image itself as the mask for transparency
    bg.paste(pokemon_resized, (pos_x, pos_y), pokemon_resized)
    
    # Add text
    draw = ImageDraw.Draw(bg)
    
    # Try to load a font
    font_path = "ChakraPetch-BoldItalic.ttf" # Modern Techno font like Chakra Petch
    
    # Dynamic font size adjustment
    # Scale font size for 2048px width
    text = pokemon_name.upper()
    max_font_size = 200  # Reduced from 250
    min_font_size = 100
    margin_x = 100 # Total horizontal margin
    
    font_size = max_font_size
    font = None
    
    while font_size >= min_font_size:
        try:
            font = ImageFont.truetype(font_path, font_size)
        except IOError:
            print(f"Warning: {font_path} not found, trying system fonts.")
            try:
                font = ImageFont.truetype("C:/Windows/Fonts/arialbd.ttf", font_size)
            except IOError:
                font = ImageFont.load_default()
                print("Warning: Arial Bold font not found, using default.")
                break # Default font is fixed size usually
        
        text_w = font.getbbox(text)[2] - font.getbbox(text)[0]
        if text_w <= (bg_w - margin_x):
            break
        font_size -= 10 # Faster step down
    
    # Recalculate text size with the final font
    bbox = font.getbbox(text)
    text_w = bbox[2] - bbox[0]
    text_h = bbox[3] - bbox[1]
    
    text_x = (bg_w - text_w) // 2
    text_y = 50 # Moved up from 80
    
    # Draw text with outline
    # User requested style: White text with Cyan outline (and maybe black outer glow)
    # Scale strokes
    
    # 1. Outer Black Stroke
    stroke_width_outer = 20 # Scaled
    draw.text((text_x, text_y), text, font=font, fill="black", stroke_width=stroke_width_outer, stroke_fill="black")

    # 2. Middle Cyan Stroke
    stroke_width_inner = 12 # Scaled
    # Cyan color: #00FFFF or "cyan"
    draw.text((text_x, text_y), text, font=font, fill="cyan", stroke_width=stroke_width_inner, stroke_fill="cyan")
    
    # 3. Inner White Fill
    draw.text((text_x, text_y), text, font=font, fill="white")
    
    # Save
    bg.save(output_path)
    print(f"Saved to {output_path}")

if __name__ == "__main__":
    if len(sys.argv) == 4:
        # Usage: python compose_image.py <pokemon_image_path> <pokemon_name> <output_path>
        # Background is hardcoded or could be arg 4
        bg_file = "ChatGPT Image 2025年12月13日 10_28_03.png"
        poke_file = sys.argv[1]
        name = sys.argv[2]
        out_file = sys.argv[3]
        create_pokemon_card(bg_file, poke_file, name, out_file)
    else:
        # Default test
        bg_file = "ChatGPT Image 2025年12月13日 10_28_03.png"
        poke_file = "mewtwo.png"
        output_file = "output_mewtwo.png"
        
        create_pokemon_card(bg_file, poke_file, "MEWTWO", output_file)
