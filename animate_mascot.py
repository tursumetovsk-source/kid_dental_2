import math
from PIL import Image, ImageChops, ImageFilter, ImageDraw

def main():
    img_path = "/Users/user/.gemini/antigravity/scratch/kid_dental_2/static/images/mascot-tooth.png"
    src = Image.open(img_path).convert("RGBA")
    W, H = src.size # 1230, 1278
    
    # We can create masks for each part
    # Left Arm (Peace sign):
    # Shoulder joint at approx (290, 400)
    mask_arm_left = Image.new("L", (W, H), 0)
    draw_al = ImageDraw.Draw(mask_arm_left)
    # Polygon covering left arm
    draw_al.polygon([
        (0, 0), (330, 0), (330, 360), (270, 440), (180, 430), (0, 350)
    ], fill=255)
    
    # Right Arm (Holding bottle):
    # Shoulder joint at approx (800, 420)
    mask_arm_right = Image.new("L", (W, H), 0)
    draw_ar = ImageDraw.Draw(mask_arm_right)
    draw_ar.polygon([
        (760, 100), (1230, 100), (1230, 600), (790, 560), (750, 420)
    ], fill=255)

    # Left Leg (Front sneaker):
    # Hip joint at approx (410, 680)
    mask_leg_left = Image.new("L", (W, H), 0)
    draw_ll = ImageDraw.Draw(mask_leg_left)
    draw_ll.polygon([
        (0, 600), (450, 600), (430, 720), (340, 750), (100, 1100), (0, 1100)
    ], fill=255)

    # Right Leg (Back sneaker):
    # Hip joint at approx (610, 760)
    mask_leg_right = Image.new("L", (W, H), 0)
    draw_lr = ImageDraw.Draw(mask_leg_right)
    draw_lr.polygon([
        (470, 740), (800, 680), (900, 950), (800, 1278), (470, 1278)
    ], fill=255)

    # Sparkle 1 (Top left): (340, 40) to (430, 150)
    mask_sparkle1 = Image.new("L", (W, H), 0)
    ImageDraw.Draw(mask_sparkle1).ellipse([340, 30, 440, 150], fill=255)

    # Sparkle 2 (Mid left): (200, 520) to (270, 610)
    mask_sparkle2 = Image.new("L", (W, H), 0)
    ImageDraw.Draw(mask_sparkle2).ellipse([200, 520, 280, 620], fill=255)

    # Sparkle 3 (Right): (680, 540) to (760, 640)
    mask_sparkle3 = Image.new("L", (W, H), 0)
    ImageDraw.Draw(mask_sparkle3).ellipse([680, 540, 760, 640], fill=255)

    # Combined limbs mask
    mask_all_limbs = Image.new("L", (W, H), 0)
    for m in [mask_arm_left, mask_arm_right, mask_leg_left, mask_leg_right, mask_sparkle1, mask_sparkle2, mask_sparkle3]:
        mask_all_limbs = ImageChops.lighter(mask_all_limbs, m)

    # Invert to get body mask
    mask_body = ImageChops.invert(mask_all_limbs)

    # Extract layers
    def extract_layer(mask):
        res = Image.new("RGBA", (W, H), (0,0,0,0))
        src_a = src.split()[3]
        combined_a = ImageChops.multiply(src_a, mask)
        res.paste(src, (0,0), combined_a)
        return res

    layer_body = extract_layer(mask_body)
    layer_arm_left = extract_layer(mask_arm_left)
    layer_arm_right = extract_layer(mask_arm_right)
    layer_leg_left = extract_layer(mask_leg_left)
    layer_leg_right = extract_layer(mask_leg_right)
    layer_sparkle1 = extract_layer(mask_sparkle1)
    layer_sparkle2 = extract_layer(mask_sparkle2)
    layer_sparkle3 = extract_layer(mask_sparkle3)

    # Helper function to rotate an image around an arbitrary pivot point (px, py)
    def rotate_at_pivot(img, angle_deg, px, py, scale=(1.0, 1.0), translate=(0, 0)):
        # Crop bounding box of img or transform
        # We can use affine transformation matrix
        # Or place onto an enlarged canvas centered at (px, py)
        # Using PIL: translate so pivot is at center, rotate, scale, translate back
        cx, cy = W // 2, H // 2
        # Offset to center pivot
        dx = cx - px
        dy = cy - py

        # Shift
        shifted = Image.new("RGBA", (W, H), (0,0,0,0))
        shifted.paste(img, (int(dx), int(dy)), img)

        # Scale & Rotate around center
        # PIL rotate rotates around center of image
        rotated = shifted.rotate(angle_deg, resample=Image.Resampling.BICUBIC, expand=False)
        
        if scale != (1.0, 1.0):
            sw = max(1, int(W * scale[0]))
            sh = max(1, int(H * scale[1]))
            scaled = rotated.resize((sw, sh), resample=Image.Resampling.BICUBIC)
            # Center back
            res = Image.new("RGBA", (W, H), (0,0,0,0))
            sx = (W - sw) // 2
            sy = (H - sh) // 2
            res.paste(scaled, (sx, sy), scaled)
            rotated = res

        # Shift back
        final_img = Image.new("RGBA", (W, H), (0,0,0,0))
        fx = -dx + translate[0]
        fy = -dy + translate[1]
        final_img.paste(rotated, (int(fx), int(fy)), rotated)
        return final_img

    num_frames = 24
    frames = []

    # Downscale target size for optimal web GIF performance and crispness (e.g., 600x624)
    target_w = 600
    target_h = int(H * (target_w / W))

    for frame_idx in range(num_frames):
        t = frame_idx / num_frames # 0.0 to 1.0
        phase = t * 2 * math.pi

        # 1. Body motion: Bouncy vertical bobbing & squash/stretch
        body_y = math.sin(phase * 2) * 14 # 2 beats per loop
        body_squash = 1.0 + math.sin(phase * 2) * 0.03
        body_stretch = 1.0 - math.sin(phase * 2) * 0.02
        body_rot = math.sin(phase) * 3.5 # subtle roll

        # 2. Left Arm (Peace sign): swings & waves enthusiastically
        # Pivot: shoulder at (290, 390)
        arm_l_rot = math.sin(phase) * 16 + math.cos(phase * 2) * 4
        arm_l_pivot = (290, 390)

        # 3. Right Arm (Bottle): pumps to the rhythm
        # Pivot: shoulder at (800, 420)
        arm_r_rot = -math.sin(phase) * 14 + math.sin(phase * 2) * 6
        arm_r_pivot = (800, 420)

        # 4. Left Leg (Front sneaker): bobs / steps
        # Pivot: hip at (410, 680)
        leg_l_rot = math.sin(phase) * 10 - math.sin(phase * 2) * 5
        leg_l_pivot = (410, 680)

        # 5. Right Leg (Back sneaker): taps / flexes
        # Pivot: hip at (610, 760)
        leg_r_rot = -math.sin(phase) * 8 + math.sin(phase * 2) * 4
        leg_r_pivot = (610, 760)

        # 6. Sparkles: pulse and twinkle
        s1_scale = 1.0 + math.sin(phase * 3) * 0.25
        s2_scale = 1.0 + math.cos(phase * 3 + 1) * 0.3
        s3_scale = 1.0 + math.sin(phase * 3 + 2) * 0.25

        # Render frame layers from back to front
        frame = Image.new("RGBA", (W, H), (0,0,0,0))

        # Back sparkle
        s3 = rotate_at_pivot(layer_sparkle3, frame_idx * 5, 720, 590, scale=(s3_scale, s3_scale), translate=(0, int(body_y * 0.5)))
        frame.paste(s3, (0,0), s3)

        # Right leg (behind body)
        rl = rotate_at_pivot(layer_leg_right, leg_r_rot, leg_r_pivot[0], leg_r_pivot[1], translate=(0, int(body_y * 0.7)))
        frame.paste(rl, (0,0), rl)

        # Left leg (behind body)
        ll = rotate_at_pivot(layer_leg_left, leg_l_rot, leg_l_pivot[0], leg_l_pivot[1], translate=(0, int(body_y * 0.7)))
        frame.paste(ll, (0,0), ll)

        # Body (center)
        b = rotate_at_pivot(layer_body, body_rot, W // 2, H // 2, scale=(body_stretch, body_squash), translate=(0, int(body_y)))
        frame.paste(b, (0,0), b)

        # Left Arm (Peace sign in front)
        al = rotate_at_pivot(layer_arm_left, arm_l_rot + body_rot, arm_l_pivot[0], arm_l_pivot[1], translate=(0, int(body_y)))
        frame.paste(al, (0,0), al)

        # Right Arm (Bottle in front)
        ar = rotate_at_pivot(layer_arm_right, arm_r_rot + body_rot, arm_r_pivot[0], arm_r_pivot[1], translate=(0, int(body_y)))
        frame.paste(ar, (0,0), ar)

        # Front Sparkles
        s1 = rotate_at_pivot(layer_sparkle1, -frame_idx * 6, 390, 90, scale=(s1_scale, s1_scale))
        frame.paste(s1, (0,0), s1)

        s2 = rotate_at_pivot(layer_sparkle2, frame_idx * 7, 240, 570, scale=(s2_scale, s2_scale))
        frame.paste(s2, (0,0), s2)

        # Resize for smooth, optimized GIF output
        resized_frame = frame.resize((target_w, target_h), resample=Image.Resampling.LANCZOS)
        frames.append(resized_frame)

    print(f"Generated {len(frames)} animated frames!")

    # Save as animated GIF with transparency
    # For PIL transparency in GIF, convert RGBA frames with proper palette
    gif_frames = []
    for f in frames:
        # Create a clean palette with transparency index 0
        alpha = f.split()[3]
        mask = Image.eval(alpha, lambda a: 255 if a > 128 else 0)
        
        # Convert RGB with adaptive palette
        rgb_img = Image.new("RGB", f.size, (252, 216, 218)) # Match site header bg color for anti-aliasing edge blending
        rgb_img.paste(f, mask=alpha)
        
        p_img = rgb_img.convert("P", palette=Image.Palette.ADAPTIVE, colors=255)
        # Set transparent color
        p_img.paste(255, ImageChops.invert(mask))
        p_img.info["transparency"] = 255
        gif_frames.append(p_img)

    out_main = "/Users/user/.gemini/antigravity/scratch/kid_dental_2/static/images/mascot-main-2.gif"
    out_video = "/Users/user/.gemini/antigravity/scratch/kid_dental_2/static/images/mascot-video.gif"
    out_tooth = "/Users/user/.gemini/antigravity/scratch/kid_dental_2/static/images/mascot-tooth.gif"

    gif_frames[0].save(
        out_main,
        save_all=True,
        append_images=gif_frames[1:],
        duration=50, # 50ms per frame = 20 fps, 1.2s seamless loop
        loop=0,
        disposal=2,
        transparency=255
    )
    gif_frames[0].save(
        out_video,
        save_all=True,
        append_images=gif_frames[1:],
        duration=50,
        loop=0,
        disposal=2,
        transparency=255
    )
    gif_frames[0].save(
        out_tooth,
        save_all=True,
        append_images=gif_frames[1:],
        duration=50,
        loop=0,
        disposal=2,
        transparency=255
    )

    print("Successfully saved animated mascot GIF to mascot-main-2.gif and mascot-video.gif!")

if __name__ == "__main__":
    main()
