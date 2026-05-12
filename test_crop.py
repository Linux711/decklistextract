#!/usr/bin/env python3
"""
Test script to crop a single card from the image.
"""

from PIL import Image, ImageDraw
import sys

def test_crop(input_path, output_path):
    # Open the input image
    img = Image.open(input_path)

    # Ensure RGBA
    if img.mode != 'RGBA':
        img = img.convert('RGBA')

    # Crop coordinates: (x, y, w, h)
    # Example: x=246, y=69, w=393, h=115
    x = 220
    y = 455
    w = 83
    h = 139
    # Convert to (left, upper, right, lower)
    coords = (x, y, x + w, y + h)

    # Crop the card
    card = img.crop(coords)

    # Create a rounded mask
    mask = Image.new('L', (w, h), 0)
    draw = ImageDraw.Draw(mask)
    radius = min(w, h) // 15  # Adjust for more/less rounding
    draw.rounded_rectangle([0, 0, w, h], radius=radius, fill=255)

    # Apply the mask to the card
    card.putalpha(mask)

    # Save as PNG
    card.save(output_path, 'PNG')
    print(f"Saved cropped card to {output_path}")

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python test_crop.py <input_image> <output_image>")
        sys.exit(1)

    input_path = sys.argv[1]
    output_path = sys.argv[2]

    test_crop(input_path, output_path)