from PIL import Image

bg_path = "ChatGPT Image 2025年12月13日 10_28_03.png"
fg_path = "mewtwo.png"

bg = Image.open(bg_path)
fg = Image.open(fg_path)

print(f"Background size: {bg.size}")
print(f"Foreground size: {fg.size}")
