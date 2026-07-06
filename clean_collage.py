import os
from PIL import Image

def flood_fill_alpha(img_path, output_path):
    img = Image.open(img_path).convert("RGBA")
    w, h = img.size
    pixels = img.load()
    
    visited = set()
    queue = []
    
    # Seed along the left, right, top, and bottom edges to capture the background
    for y in range(h):
        seeds = [(0, y), (w-1, y)]
        for sx, sy in seeds:
            visited.add((sx, sy))
            queue.append((sx, sy))
            
    for x in range(w):
        seeds = [(x, 0), (x, h-1)]
        for sx, sy in seeds:
            if (sx, sy) not in visited:
                visited.add((sx, sy))
                queue.append((sx, sy))
                
    while queue:
        cx, cy = queue.pop(0)
        curr_pixel = pixels[cx, cy]
        
        # Set alpha to 0 (fully transparent)
        pixels[cx, cy] = (curr_pixel[0], curr_pixel[1], curr_pixel[2], 0)
        
        # Check 4-neighbors
        for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
            nx, ny = cx + dx, cy + dy
            if 0 <= nx < w and 0 <= ny < h and (nx, ny) not in visited:
                neighbor_pixel = pixels[nx, ny]
                r, g, b, a = neighbor_pixel
                
                # Check if it is a background pixel (light blue or white gradient)
                is_bg = (r > 150 and g > 210 and b > 220) or (r > 240 and g > 240 and b > 240)
                
                # Make sure we don't cross the dark blue double circle borders
                is_boundary = (r < 100 and b > 110)
                
                if is_bg and not is_boundary:
                    visited.add((nx, ny))
                    queue.append((nx, ny))
                    
    # Save the output image
    img.save(output_path, "PNG")
    print(f"Successfully saved transparent image to {output_path}")

if __name__ == "__main__":
    src = r"C:\Users\G H O S T\.gemini\antigravity\brain\830a6650-f789-4535-b379-b53e8d6a6fd5\media__1783343445913.jpg"
    dest = r"assets\images\dr-ayesha-surgery.png"
    flood_fill_alpha(src, dest)
