import cv2
import numpy as np
from PIL import Image
import os

def slice_reviews_v2(image_path, output_prefix):
    img = cv2.imread(image_path)
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    
    # A gap is a row where all pixels are almost the exact same color.
    row_stds = np.std(gray, axis=1)
    is_gap = row_stds < 2
    
    gaps = []
    in_gap = False
    gap_start = 0
    
    for i, val in enumerate(is_gap):
        if val and not in_gap:
            in_gap = True
            gap_start = i
        elif not val and in_gap:
            in_gap = False
            gap_end = i
            # Require the gap to be at least 15 pixels thick to avoid random solid lines
            if gap_end - gap_start >= 15:
                gaps.append((gap_start + gap_end) // 2)
                
    # Also add top and bottom
    splits = [0] + gaps + [img.shape[0]]
    
    # Filter out splits that are too close to each other (e.g., < 200 pixels)
    # Since reviews are usually at least 200 pixels tall
    filtered_splits = [splits[0]]
    for s in splits[1:]:
        if s - filtered_splits[-1] > 200:
            filtered_splits.append(s)
    # Ensure the last split is the bottom of the image if not already close
    if img.shape[0] - filtered_splits[-1] > 200:
        filtered_splits.append(img.shape[0])
    else:
        filtered_splits[-1] = img.shape[0]
        
    print(f"Filtered splits: {filtered_splits}")
    
    pil_img = Image.open(image_path)
    
    # Clean previous slices
    for f in os.listdir("d:/Gokulam/images"):
        if f.startswith("review_slice_"):
            os.remove(f"d:/Gokulam/images/{f}")
            
    saved_files = []
    for i in range(len(filtered_splits) - 1):
        top = filtered_splits[i]
        bottom = filtered_splits[i+1]
        
        cropped = pil_img.crop((0, top, img.shape[1], bottom))
        out_name = f"{output_prefix}_{len(saved_files)+1}.png"
        cropped.save(out_name)
        saved_files.append(out_name)
        print(f"Saved {out_name} (height: {bottom - top})")

slice_reviews_v2("d:/Gokulam/images/Reviews.png", "d:/Gokulam/images/review_slice")
