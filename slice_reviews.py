import cv2
import numpy as np
from PIL import Image

def slice_reviews(image_path, output_prefix):
    # Load image using OpenCV
    img = cv2.imread(image_path)
    if img is None:
        print("Failed to load image")
        return
        
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    
    # In GMB reviews, the background is usually white (#FFFFFF) or very light grey.
    # Let's find rows where almost all pixels are very bright.
    # A row is considered a "gap" if its variance is very low and its mean is very high.
    
    # Calculate row-wise mean and std
    row_means = np.mean(gray, axis=1)
    row_stds = np.std(gray, axis=1)
    
    # We want rows that are white-ish and flat (low std)
    # Let's say a gap is where mean > 240 and std < 5
    is_gap = (row_means > 240) & (row_stds < 5)
    
    # We want to find contiguous blocks of gaps to split the image
    # We will find the middle of each gap block.
    
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
            # If the gap is thick enough (e.g., > 10 pixels), we consider it a separator
            if gap_end - gap_start > 10:
                gaps.append((gap_start + gap_end) // 2)
                
    print(f"Found {len(gaps)} potential splits: {gaps}")
    
    # If we didn't find clear gaps, fallback to splitting by 3 equal parts (common for 3 reviews)
    if len(gaps) == 0:
        print("No clear gaps found, splitting into 3 equal parts.")
        h = img.shape[0]
        gaps = [h // 3, 2 * h // 3]
        
    # We will slice the image using these gaps
    # Add 0 at the beginning and height at the end
    splits = [0] + gaps + [img.shape[0]]
    
    pil_img = Image.open(image_path)
    saved_files = []
    
    for i in range(len(splits) - 1):
        top = splits[i]
        bottom = splits[i+1]
        
        # Don't save tiny slices
        if bottom - top < 50:
            continue
            
        cropped = pil_img.crop((0, top, img.shape[1], bottom))
        out_name = f"{output_prefix}_{len(saved_files)+1}.png"
        cropped.save(out_name)
        saved_files.append(out_name)
        print(f"Saved {out_name} (height: {bottom - top})")

slice_reviews("d:/Gokulam/images/Reviews.png", "d:/Gokulam/images/review_slice")
