import os
from PIL import Image

def find_islands(img):
    W, H = img.size
    alpha = img.split()[3]
    visited = bytearray(W * H)
    alpha_bytes = alpha.tobytes()

    islands = []

    for y in range(H):
        for x in range(W):
            idx = y * W + x
            if alpha_bytes[idx] > 20 and not visited[idx]:
                # Start flood fill (BFS)
                min_x, max_x = x, x
                min_y, max_y = y, y
                queue = [(x, y)]
                visited[idx] = 1

                while queue:
                    cx, cy = queue.pop()
                    if cx < min_x: min_x = cx
                    if cx > max_x: max_x = cx
                    if cy < min_y: min_y = cy
                    if cy > max_y: max_y = cy

                    # 4-neighbors
                    for nx, ny in ((cx+1, cy), (cx-1, cy), (cx, cy+1), (cx, cy-1)):
                        if 0 <= nx < W and 0 <= ny < H:
                            nidx = ny * W + nx
                            if alpha_bytes[nidx] > 20 and not visited[nidx]:
                                visited[nidx] = 1
                                queue.append((nx, ny))

                w_box = max_x - min_x + 1
                h_box = max_y - min_y + 1
                # Ignore tiny noise (< 10x10)
                if w_box > 15 and h_box > 15:
                    islands.append((min_x, min_y, max_x + 1, max_y + 1))

    return islands

def main():
    img_path = "/Users/user/.gemini/antigravity/scratch/kid_dental_2/static/images/mascot-parts.png"
    src = Image.open(img_path).convert("RGBA")
    out_dir = "/Users/user/.gemini/antigravity/scratch/kid_dental_2/static/images/mascot_parts"
    os.makedirs(out_dir, exist_ok=True)

    islands = find_islands(src)
    print(f"Found {len(islands)} distinct parts!")

    for i, box in enumerate(islands):
        part = src.crop(box)
        w, h = part.size
        print(f"Part {i}: box={box}, size={w}x{h}, center=({box[0]+w//2}, {box[1]+h//2})")
        part.save(os.path.join(out_dir, f"part_{i}_{w}x{h}.png"))

if __name__ == "__main__":
    main()
