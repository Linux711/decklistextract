#!/usr/bin/env python3
"""
Image Crop and Rearrange Tool

This script crops a fixed-format image into 33 predefined rectangular sections,
then rearranges and composites them onto a new canvas with a transparent background.
The final output is saved as a PNG file.

Usage:
    python crop_and_rearrange.py <input_image> <output_image>

Requirements:
    - Pillow (PIL)
    - Install with: pip install pillow
"""

from PIL import Image
import sys
import os

def crop_and_rearrange(input_path, output_path):
    """
    Crop the input image into 33 sections and rearrange them on a new canvas.

    Args:
        input_path (str): Path to the input image
        output_path (str): Path to save the output PNG
    """

    # Open the input image
    try:
        img = Image.open(input_path)
    except IOError:
        print(f"Error: Cannot open image {input_path}")
        return

    # Ensure the image has an alpha channel for transparency
    if img.mode != 'RGBA':
        img = img.convert('RGBA')

    # Define crop coordinates for 33 cards
    # These are example coordinates - replace with your actual predefined coordinates
    # Format: (left, upper, right, lower) - pixel coordinates
    crop_coords = [
        # Row 1
        (0, 0, 100, 150),
        (100, 0, 200, 150),
        (200, 0, 300, 150),
        (300, 0, 400, 150),
        (400, 0, 500, 150),
        (500, 0, 600, 150),
        # Row 2
        (0, 150, 100, 300),
        (100, 150, 200, 300),
        (200, 150, 300, 300),
        (300, 150, 400, 300),
        (400, 150, 500, 300),
        (500, 150, 600, 300),
        # Row 3
        (0, 300, 100, 450),
        (100, 300, 200, 450),
        (200, 300, 300, 450),
        (300, 300, 400, 450),
        (400, 300, 500, 450),
        (500, 300, 600, 450),
        # Row 4
        (0, 450, 100, 600),
        (100, 450, 200, 600),
        (200, 450, 300, 600),
        (300, 450, 400, 600),
        (400, 450, 500, 600),
        (500, 450, 600, 600),
        # Row 5
        (0, 600, 100, 750),
        (100, 600, 200, 750),
        (200, 600, 300, 750),
        (300, 600, 400, 750),
        (400, 600, 500, 750),
        (500, 600, 600, 750),
        # Row 6 (last card)
        (0, 750, 100, 900),
        (100, 750, 200, 900),
        (200, 750, 300, 900),
    ]

    # Verify we have exactly 33 coordinates
    if len(crop_coords) != 33:
        print(f"Error: Expected 33 crop coordinates, got {len(crop_coords)}")
        return

    # Crop the sections
    cards = []
    for i, coords in enumerate(crop_coords):
        try:
            card = img.crop(coords)
            cards.append(card)
        except Exception as e:
            print(f"Error cropping card {i+1}: {e}")
            return

    # Define the layout for rearranging on new canvas
    # Example: 6 rows of 5 cards, with 3 in the last row
    # Adjust these positions based on your desired layout
    layout_positions = [
        # Row 1: 5 cards
        (0, 0), (105, 0), (210, 0), (315, 0), (420, 0),
        # Row 2: 5 cards
        (0, 155), (105, 155), (210, 155), (315, 155), (420, 155),
        # Row 3: 5 cards
        (0, 310), (105, 310), (210, 310), (315, 310), (420, 310),
        # Row 4: 5 cards
        (0, 465), (105, 465), (210, 465), (315, 465), (420, 465),
        # Row 5: 5 cards
        (0, 620), (105, 620), (210, 620), (315, 620), (420, 620),
        # Row 6: 3 cards (centered)
        (105, 775), (210, 775), (315, 775),
        # Row 7: 5 cards
        (0, 930), (105, 930), (210, 930), (315, 930), (420, 930),
    ]

    # Calculate canvas size
    # Assuming all cards are the same size (100x150 in this example)
    card_width = 100
    card_height = 150
    canvas_width = 525  # 5 cards * 100 + 4 gaps * 5
    canvas_height = 1085  # 7 rows * 150 + 6 gaps * 5

    # Create new canvas with transparent background
    canvas = Image.new('RGBA', (canvas_width, canvas_height), (0, 0, 0, 0))

    # Paste cards onto canvas
    for card, position in zip(cards, layout_positions):
        canvas.paste(card, position, card)  # Use card as mask for transparency

    # Save the result
    try:
        canvas.save(output_path, 'PNG')
        print(f"Successfully saved rearranged image to {output_path}")
    except IOError:
        print(f"Error: Cannot save image to {output_path}")

def main():
    if len(sys.argv) != 3:
        print("Usage: python crop_and_rearrange.py <input_image> <output_image>")
        print("Example: python crop_and_rearrange.py input.png output.png")
        sys.exit(1)

    input_path = sys.argv[1]
    output_path = sys.argv[2]

    if not os.path.exists(input_path):
        print(f"Error: Input file {input_path} does not exist")
        sys.exit(1)

    crop_and_rearrange(input_path, output_path)

if __name__ == "__main__":
    main()