import os
try:
    from PIL import Image
except ImportError:
    print("Pillow not installed. Run: pip install Pillow")
    exit(1)

def make_collage():
    directory = r"c:\Users\OLUGBADE TAYO\Desktop\AI coding class\LeadGreen V1\Frontend"
    
    base_images = [
        "Okoya.jpeg",
        "samuel.jpg",
        "Markson.png"
    ]
    
    loaded = []
    for name in base_images:
        path = os.path.join(directory, name)
        if os.path.exists(path):
            try:
                img = Image.open(path).convert("RGB")
                loaded.append(img)
            except Exception as e:
                pass

    if not loaded:
        print("No faces found to stitch.")
        return
        
    cols = 5
    rows = 14
    total_images = cols * rows
    img_w, img_h = 240, 320
    
    images = []
    for i in range(total_images):
        src = loaded[i % len(loaded)]
        w, h = src.size
        aspect = w / h
        target_aspect = img_w / img_h
        
        if aspect > target_aspect:
            new_w = int(target_aspect * h)
            offset = (w - new_w) / 2
            crop_box = (offset, 0, w - offset, h)
        else:
            new_h = int(w / target_aspect)
            offset = (h - new_h) / 2
            crop_box = (0, offset, w, h - offset)
            
        cropped = src.crop(crop_box).resize((img_w, img_h), Image.Resampling.LANCZOS)
        images.append(cropped)

    padding = 10
    canvas_w = (cols * img_w) + ((cols + 1) * padding)
    canvas_h = (rows * img_h) + ((rows + 1) * padding)
    
    collage = Image.new("RGB", (canvas_w, canvas_h), (248, 249, 250))

    for i, img in enumerate(images):
        col = i % cols
        row = i // cols
        x = padding + col * (img_w + padding)
        y = padding + row * (img_h + padding)
        collage.paste(img, (x, y))

    output_path = os.path.join(directory, "database_collage.png")
    collage.save(output_path)
    print("SUCCESS")

if __name__ == "__main__":
    make_collage()
