import os
from PIL import Image

def main():
    parts_dir = "/Users/user/.gemini/antigravity/scratch/kid_dental_2/static/images/mascot_parts"
    
    # Load parts
    body = Image.open(f"{parts_dir}/body.png").convert("RGBA")
    glasses = Image.open(f"{parts_dir}/glasses.png").convert("RGBA")
    eyebrow_l = Image.open(f"{parts_dir}/eyebrow_l.png").convert("RGBA")
    eyebrow_r = Image.open(f"{parts_dir}/eyebrow_r.png").convert("RGBA")
    mouth = Image.open(f"{parts_dir}/mouth.png").convert("RGBA")
    bottle = Image.open(f"{parts_dir}/bottle.png").convert("RGBA")
    arm_l_seg = Image.open(f"{parts_dir}/arm_l_seg.png").convert("RGBA")
    hand_peace = Image.open(f"{parts_dir}/hand_peace.png").convert("RGBA")
    arm_r_seg = Image.open(f"{parts_dir}/arm_r_seg.png").convert("RGBA")
    hand_r_grip = Image.open(f"{parts_dir}/hand_r_grip.png").convert("RGBA")
    leg_l = Image.open(f"{parts_dir}/leg_l.png").convert("RGBA")
    leg_r = Image.open(f"{parts_dir}/leg_r.png").convert("RGBA")
    sparkle_blue = Image.open(f"{parts_dir}/sparkle_blue.png").convert("RGBA")
    sparkle_pink = Image.open(f"{parts_dir}/sparkle_pink.png").convert("RGBA")

    # Assemble Left Arm (Arm + Peace Hand)
    # Peace hand overlaps with arm cuff
    arm_left_full = Image.new("RGBA", (300, 350), (0,0,0,0))
    # Arm segment (109 x 220)
    # Hand peace (154 x 217)
    arm_left_full.paste(arm_l_seg, (110, 110), arm_l_seg)
    arm_left_full.paste(hand_peace, (10, 10), hand_peace)
    arm_left_full.save(f"{parts_dir}/arm_left_assembled.png")

    # Assemble Right Arm (Arm + Hand Grip + Bottle)
    arm_right_full = Image.new("RGBA", (360, 420), (0,0,0,0))
    # Arm segment (134 x 176)
    # Hand grip (151 x 161)
    # Bottle (147 x 273)
    arm_right_full.paste(arm_r_seg, (10, 150), arm_r_seg)
    arm_right_full.paste(bottle, (140, 10), bottle)
    arm_right_full.paste(hand_r_grip, (100, 120), hand_r_grip)
    arm_right_full.save(f"{parts_dir}/arm_right_assembled.png")

    # Reference assembly test
    canvas = Image.new("RGBA", (900, 900), (0,0,0,0))
    
    # 1. Legs (behind body)
    canvas.paste(leg_l, (70, 420), leg_l)
    canvas.paste(leg_r, (360, 430), leg_r)

    # 2. Body (center)
    canvas.paste(body, (220, 120), body)

    # 3. Face
    canvas.paste(mouth, (390, 320), mouth)
    canvas.paste(glasses, (260, 185), glasses)
    canvas.paste(eyebrow_l, (320, 125), eyebrow_l)
    canvas.paste(eyebrow_r, (490, 120), eyebrow_r)

    # 4. Arms
    canvas.paste(arm_left_full, (50, 60), arm_left_full)
    canvas.paste(arm_right_full, (540, 60), arm_right_full)

    # 5. Sparkles
    canvas.paste(sparkle_blue, (180, 20), sparkle_blue)
    canvas.paste(sparkle_pink, (120, 310), sparkle_pink)
    canvas.paste(sparkle_pink, (660, 460), sparkle_pink)

    canvas.save(f"{parts_dir}/test_assembled_character.png")
    print("Saved test_assembled_character.png successfully!")

if __name__ == "__main__":
    main()
