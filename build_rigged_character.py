import os
import math
from PIL import Image, ImageChops

def main():
    src_path = "/Users/user/.gemini/antigravity/scratch/kid_dental_2/static/images/mascot-parts.png"
    src = Image.open(src_path).convert("RGBA")
    
    parts_dir = "/Users/user/.gemini/antigravity/scratch/kid_dental_2/static/images/mascot_parts"
    os.makedirs(parts_dir, exist_ok=True)

    # Coordinates from island detection
    # Part 2: Body (616, 68, 1091, 542)
    body = src.crop((616, 68, 1091, 542))
    body.save(os.path.join(parts_dir, "body.png"))

    # Part 6: Sunglasses (1108, 156, 1514, 296)
    glasses = src.crop((1108, 156, 1514, 296))
    glasses.save(os.path.join(parts_dir, "glasses.png"))

    # Part 4 & 3: Eyebrows
    eyebrow_l = src.crop((1154, 71, 1256, 116))
    eyebrow_r = src.crop((1326, 69, 1430, 116))
    eyebrow_l.save(os.path.join(parts_dir, "eyebrow_l.png"))
    eyebrow_r.save(os.path.join(parts_dir, "eyebrow_r.png"))

    # Part 9: Mouth (1128, 327, 1277, 459)
    mouth = src.crop((1128, 327, 1277, 459))
    mouth.save(os.path.join(parts_dir, "mouth.png"))

    # Part 8: Bottle (1343, 312, 1490, 585)
    bottle = src.crop((1343, 312, 1490, 585))
    bottle.save(os.path.join(parts_dir, "bottle.png"))

    # Part 16: Left arm segment (560, 539, 669, 759)
    # Part 14: Peace hand (684, 532, 838, 749)
    arm_l_seg = src.crop((560, 539, 669, 759))
    hand_peace = src.crop((684, 532, 838, 749))
    arm_l_seg.save(os.path.join(parts_dir, "arm_l_seg.png"))
    hand_peace.save(os.path.join(parts_dir, "hand_peace.png"))

    # Part 15: Right arm segment (1150, 533, 1284, 709)
    # Part 19: Right hand grip (1307, 610, 1458, 771)
    arm_r_seg = src.crop((1150, 533, 1284, 709))
    hand_r_grip = src.crop((1307, 610, 1458, 771))
    arm_r_seg.save(os.path.join(parts_dir, "arm_r_seg.png"))
    hand_r_grip.save(os.path.join(parts_dir, "hand_r_grip.png"))

    # Part 20: Left leg + shoe (72, 623, 320, 928)
    leg_l = src.crop((72, 623, 320, 928))
    leg_l.save(os.path.join(parts_dir, "leg_l.png"))

    # Part 21: Right leg + shoe (415, 636, 656, 979)
    leg_r = src.crop((415, 636, 656, 979))
    leg_r.save(os.path.join(parts_dir, "leg_r.png"))

    # Sparkles
    sparkle_blue = src.crop((1318, 789, 1403, 887))
    sparkle_pink = src.crop((1428, 770, 1497, 850))
    sparkle_blue.save(os.path.join(parts_dir, "sparkle_blue.png"))
    sparkle_pink.save(os.path.join(parts_dir, "sparkle_pink.png"))

    print("All individual parts saved cleanly to", parts_dir)

if __name__ == "__main__":
    main()
