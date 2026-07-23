from PIL import Image

def remove_background(image_path, output_path, bg_color=(255, 255, 255), tolerance=30):
    img = Image.open(image_path)
    img = img.convert("RGBA")
    datas = img.getdata()
    
    new_data = []
    for item in datas:
        # Check if the pixel color is close to the background color
        if (abs(item[0] - bg_color[0]) <= tolerance and 
            abs(item[1] - bg_color[1]) <= tolerance and 
            abs(item[2] - bg_color[2]) <= tolerance):
            # Change to transparent
            new_data.append((255, 255, 255, 0))
        else:
            new_data.append(item)
            
    img.putdata(new_data)
    img.save(output_path, "PNG")

remove_background("images/Gokulam.Logo.png", "images/Gokulam.Logo.png")
print("Background removed")
