#!/usr/bin/env python3
"""
Test script to crop two cards from the image using x, y, w, h.
The second crop is shifted 100 pixels to the right (x+100), all other values identical.
"""

from PIL import Image, ImageDraw
import sys

def test_crop_and_composite(input_path, output_path):
    # Open the input image
    img = Image.open(input_path)

    # Resize to 1050x1428 if needed
    target_size = (1050, 1428)
    if img.size != target_size:
        img = img.resize(target_size, Image.LANCZOS)

    # Ensure RGBA
    if img.mode != 'RGBA':
        img = img.convert('RGBA')

    # Crop parameters
    x = 220
    y = 455
    w = 83
    h = 139
    num_cards = 6
    x_shift = 100
    spacing = 17
    y_row_shift = 156
    total_cards = num_cards * 5  # 5 rows of 6 cards = 30 cards
    out_cols = 8

    # Crop all cards (flattened list)
    cards = []
    for row in range(5):
        y_row = y + row * y_row_shift
        for i in range(num_cards):
            x_i = x + i * x_shift
            coords = (x_i, y_row, x_i + w, y_row + h)
            card = img.crop(coords)
            # Create a rounded mask for each card
            mask = Image.new('L', (w, h), 0)
            draw = ImageDraw.Draw(mask)
            radius = min(w, h) // 12  # Adjust for more/less rounding
            draw.rounded_rectangle([0, 0, w, h], radius=radius, fill=255)
            card.putalpha(mask)
            cards.append(card)

    # Calculate how many rows are actually needed
    out_rows = (len(cards) + out_cols - 1) // out_cols
    # For output, rows should be stacked with only card height between them
    v_spacing = 17
    canvas_width = out_cols * w + (out_cols - 1) * spacing
    canvas_height = out_rows * h + (out_rows - 1) * v_spacing
    canvas = Image.new('RGBA', (canvas_width, canvas_height), (0, 0, 0, 0))

    # Paste cards onto canvas with spacing, row by row
    for idx, card in enumerate(cards):
        row = idx // out_cols
        col = idx % out_cols
        x_pos = col * (w + spacing)
        y_pos = row * (h + v_spacing)  # add vertical gap between rows
        canvas.paste(card, (x_pos, y_pos), card)

    # Save the composite image
    canvas.save(output_path, 'PNG')
    print(f"Saved composite image to {output_path}")

if __name__ == "__main__":
    while True:
        input_path = input("Enter input image filename (or 'q' to quit): ").strip()
        if input_path.lower() in ('q', 'quit', 'exit'):
            print("Exiting.")
            break
        output_path = 'output.png'
        try:
            test_crop_and_composite(input_path, output_path)
            print(f"Processed {input_path} -> {output_path}")
        except Exception as e:
            print(f"Error: {e}")
