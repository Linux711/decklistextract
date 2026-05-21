#!/usr/bin/env python3
"""
cgen.py
Crops 3 cards, each 100 pixels apart horizontally, starting 100 pixels above the first card in dlgen.py.
"""

from PIL import Image, ImageDraw
import sys

def crop_three_cards(input_path, output_path):
    # Open the input image
    img = Image.open(input_path)

    # Resize to 1050x1428 if needed
    target_size = (1050, 1428)
    if img.size != target_size:
        img = img.resize(target_size, Image.LANCZOS)

    # Ensure RGBA
    if img.mode != 'RGBA':
        img = img.convert('RGBA')

    # Card parameters (from dlgen.py, but y is 100 pixels higher, and now 60px further up and right)
    x = 307  # move 100 pixels right
    y = 156 # move 60 pixels up from previous y
    w = 125
    h = 207
    num_cards = 3
    x_shift = 141.7
    spacing = 17

    # Crop 3 cards
    cards = []
    for i in range(num_cards):
        x_i = x + i * x_shift
        left = int(round(x_i))
        upper = int(round(y))
        right = left + w
        lower = upper + h
        card = img.crop((left, upper, right, lower))
        # Rounded corners
        mask = Image.new('L', (w, h), 0)
        draw = ImageDraw.Draw(mask)
        radius = min(w, h) // 12
        draw.rounded_rectangle([0, 0, w, h], radius=radius, fill=255)
        card.putalpha(mask)
        cards.append(card)

    # Create transparent canvas for compositing
    canvas_width = num_cards * w + (num_cards - 1) * spacing
    canvas_height = h
    canvas = Image.new('RGBA', (canvas_width, canvas_height), (0, 0, 0, 0))

    # Paste cards onto canvas with spacing
    for i, card in enumerate(cards):
        x_pos = i * (w + spacing)
        canvas.paste(card, (x_pos, 0), card)

    # Save the composite image
    canvas.save(output_path, 'PNG')
    print(f"Saved composite image to {output_path}")

if __name__ == "__main__":
    input_path = input("Enter input image filename: ").strip()
    output_path = 'cgenoutput.png'
    crop_three_cards(input_path, output_path)
