import sys
from PIL import Image, ImageDraw, ImageFilter

def process_image(input_path, output_path):
    # Open the original image
    try:
        img = Image.open(input_path).convert("RGBA")
    except Exception as e:
        print(f"Error opening image: {e}")
        return

    # Create a mask for flood fill from the background
    # The flood fill will replace the outer background with a distinct color, e.g. magenta
    bg_color = (255, 0, 255, 255)
    
    # We create a new image for floodfilling since floodfill works better on RGB
    temp_img = img.convert("RGB")
    
    from PIL import ImageDraw
    # We do a floodfill from corners assuming they are background
    width, height = temp_img.size
    
    # Instead of flood fill, let's do something simpler:
    # Any pixel that is close to white AND near the edge of the image
    # Or just replace all white pixels if the user's previous script did that.
    # Actually, a better way to remove a white background and anti-aliasing halo:
    
    # We will use the alpha channel based on darkness. But this might make the image translucent.
    
    # Let's try to find the bounding box of the non-white pixels
    data = img.getdata()
    new_data = []
    
    # To remove the halo, we can make pixels transparent if they are too white
    # The user asked to remove white padding, white border, and empty transparent space.
    # So we should crop it tightly first.
    
    min_x, min_y = width, height
    max_x, max_y = 0, 0
    
    # Let's first make near-white pixels transparent
    for y in range(height):
        for x in range(width):
            r, g, b, a = img.getpixel((x, y))
            # If the pixel is very bright, it's part of the white halo or background
            if r > 240 and g > 240 and b > 240:
                new_data.append((255, 255, 255, 0))
            elif a < 10:
                new_data.append((255, 255, 255, 0))
            else:
                new_data.append((r, g, b, a))
                if x < min_x: min_x = x
                if x > max_x: max_x = x
                if y < min_y: min_y = y
                if y > max_y: max_y = y
                
    img.putdata(new_data)
    
    if min_x <= max_x and min_y <= max_y:
        # Crop to the bounding box
        img = img.crop((min_x, min_y, max_x + 1, max_y + 1))
    
    # Save the processed image
    img.save(output_path, "PNG")
    print(f"Processed {input_path} and saved to {output_path}")

# Run on the logo image
process_image("d:/Gokulam/images/Gokulam.Logo.png", "d:/Gokulam/images/Gokulam.Logo.png")
process_image("d:/Gokulam/images/og-logo.jpg", "d:/Gokulam/images/og-logo.jpg")

