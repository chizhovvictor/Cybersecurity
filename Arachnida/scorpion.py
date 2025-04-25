#!/usr/bin/env python3

import sys
import os
from PIL import Image
from PIL.ExifTags import TAGS

def extract_metadata(filepath):
    try:
        img = Image.open(filepath)
        print(f"\nFile: {filepath}")
        print("-" * 60)

        print(f"Format: {img.format}")
        print(f"Size: {img.size}")
        print(f"Mode: {img.mode}")

        exif_data = img._getexif()

        if not exif_data:
            print("No EXIF data found.")
            return

        for tag_id, value in exif_data.items():
            tag = TAGS.get(tag_id, tag_id)
            print(f"{tag:25}: {value}")

    except Exception as e:
        print(f"[!] Failed to process {filepath}: {e}")

def main():
    if len(sys.argv) < 2:
        print("Usage: ./scorpion FILE1 [FILE2 ...]")
        sys.exit(1)

    for filepath in sys.argv[1:]:
        if not os.path.isfile(filepath):
            print(f"[!] {filepath} is not a valid file.")
            continue
        extract_metadata(filepath)

if __name__ == "__main__":
    main()
