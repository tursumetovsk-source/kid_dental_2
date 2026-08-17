import os
import math
from PIL import Image, ImageChops, ImageDraw

def rotate_about_point(img, angle_deg, pivot_x, pivot_y, canvas_size=(900, 900), offset=(0, 0), scale=(1.0, 1.0)):
    """
    Places `img` on a canvas so its local pivot aligns with (pivot_x, pivot_y),
    rotates by angle_deg around that pivot, and returns the canvas.
    """
    CW, CH = canvas_size
    # Create canvas centered on pivot
    cx, cy = CW // 2, CH // 2
    dx = cx - pivot_x
    dy = cy - pivot_y

    layer = Image.new("RGBA", (CW, CH), (0,0,0,0))
    layer.paste(img, (int(dx), int(dy)), img)

    if scale != (1.0, 1.0):
        sw = max(1, int(CW * scale[0]))
        sh = max(1, int(CH * scale[1]))
        scaled = layer.resize((sw, sh), resample=Image.Resampling.BICUBIC)
        # Re-center
        layer = Image.new("RGBA", (CW, CH), (0,0,0,0))
        layer.paste(scaled, ((CW - sw)//2, (CH - sh)//2), scaled)

    rotated = layer.rotate(angle_deg, resample=Image.Resampling.BICUBIC)

    # Shift from center back to pivot position + offset
    final_canvas = Image.new("RGBA", (CW, CH), (0,0,0,0))
    fx = -dx + offset[0]
    fy = -dy + offset[1]
    final_canvas.paste(rotated, (int(fx), int(fy)), rotated)
    return final_canvas

def main():
    parts_dir = "/Users/user/.gemini/antigravity/scratch/kid_dental_2/static/images/mascot_parts"
    
    # Load parts
    body = Image.open(f"{parts_dir}/body.png").convert("RGBA")
    glasses = Image.open(f"{parts_dir}/glasses.png").convert("RGBA")
    eyebrow_l = Image.open(f"{parts_dir}/eyebrow_l.png").convert("RGBA")
    eyebrow_r = Image.open(f"{parts_dir}/eyebrow_r.png").convert("RGBA")
    mouth = Image.open(f"{parts_dir}/mouth.png").convert("RGBA")
    sparkle_blue = Image.open(f"{parts_dir}/sparkle_blue.png").convert("RGBA")
    sparkle_pink = Image.open(f"{parts_dir}/sparkle_pink.png").convert("RGBA")

    # Load assembled arms and legs
    arm_left_full = Image.open(f"{parts_dir}/arm_left_assembled.png").convert("RGBA")
    arm_right_full = Image.open(f"{parts_dir}/arm_right_assembled.png").convert("RGBA")
    leg_l = Image.open(f"{parts_dir}/leg_l.png").convert("RGBA")
    leg_r = Image.open(f"{parts_dir}/leg_r.png").convert("RGBA")

    num_frames = 28
    frames = []
    CW, CH = 900, 900

    for frame_idx in range(num_frames):
        t = frame_idx / num_frames
        phase = t * 2 * math.pi

        # 1. Rhythmic Body Motion (bounce + squash & stretch)
        body_y = math.sin(phase * 2) * 16 # 2 bounces per cycle
        body_squash = 1.0 + math.sin(phase * 2) * 0.035
        body_stretch = 1.0 - math.sin(phase * 2) * 0.025
        body_tilt = math.sin(phase) * 3.0 # subtle body roll

        # 2. Left Arm (Peace sign wave)
        # Shoulder anchor at (240, 360) in character space
        arm_l_angle = math.sin(phase) * 16.0 + math.cos(phase * 2) * 4.0
        # Arm image local shoulder anchor is at approx (210, 320)
        arm_l_layer = Image.new("RGBA", (CW, CH), (0,0,0,0))
        arm_l_layer.paste(arm_left_full, (50, 60), arm_left_full)
        arm_l_rot = rotate_about_point(
            arm_l_layer,
            arm_l_angle,
            pivot_x=240,
            pivot_y=360,
            offset=(0, int(body_y))
        )

        # 3. Right Arm (Bottle pump)
        # Shoulder anchor at (570, 370)
        arm_r_angle = -math.sin(phase) * 14.0 + math.sin(phase * 2) * 6.0
        arm_r_layer = Image.new("RGBA", (CW, CH), (0,0,0,0))
        arm_r_layer.paste(arm_right_full, (540, 60), arm_right_full)
        arm_r_rot = rotate_about_point(
            arm_r_layer,
            arm_r_angle,
            pivot_x=570,
            pivot_y=370,
            offset=(0, int(body_y))
        )

        # 4. Left Leg (Front sneaker bounce)
        # Hip anchor at (280, 500)
        leg_l_angle = math.sin(phase) * 9.0 - math.sin(phase * 2) * 4.0
        leg_l_layer = Image.new("RGBA", (CW, CH), (0,0,0,0))
        leg_l_layer.paste(leg_l, (70, 420), leg_l)
        leg_l_rot = rotate_about_point(
            leg_l_layer,
            leg_l_angle,
            pivot_x=280,
            pivot_y=500,
            offset=(0, int(body_y * 0.6))
        )

        # 5. Right Leg (Back sneaker flex)
        # Hip anchor at (480, 520)
        leg_r_angle = -math.sin(phase) * 8.0 + math.sin(phase * 2) * 3.0
        leg_r_layer = Image.new("RGBA", (CW, CH), (0,0,0,0))
        leg_r_layer.paste(leg_r, (360, 430), leg_r)
        leg_r_rot = rotate_about_point(
            leg_r_layer,
            leg_r_angle,
            pivot_x=480,
            pivot_y=520,
            offset=(0, int(body_y * 0.6))
        )

        # 6. Body + Face Assembly
        body_canvas = Image.new("RGBA", (CW, CH), (0,0,0,0))
        body_canvas.paste(body, (220, 120), body)
        
        # Mouth with tongue bounce
        mouth_y = int(320 + math.sin(phase * 2) * 2)
        body_canvas.paste(mouth, (390, mouth_y), mouth)

        # Sunglasses with groove tilt
        glasses_y = int(185 + math.sin(phase * 2) * 1)
        body_canvas.paste(glasses, (260, glasses_y), glasses)

        # Eyebrows raising expressively
        eyebrow_y = int(125 + math.sin(phase * 2) * 3)
        body_canvas.paste(eyebrow_l, (320, eyebrow_y), eyebrow_l)
        body_canvas.paste(eyebrow_r, (490, eyebrow_y - 5), eyebrow_r)

        body_rot = rotate_about_point(
            body_canvas,
            body_tilt,
            pivot_x=450,
            pivot_y=350,
            offset=(0, int(body_y)),
            scale=(body_stretch, body_squash)
        )

        # 7. Sparkles with twinkling scale & spin
        s_blue_scale = 1.0 + math.sin(phase * 3) * 0.3
        s_pink1_scale = 1.0 + math.cos(phase * 3 + 1) * 0.35
        s_pink2_scale = 1.0 + math.sin(phase * 3 + 2) * 0.3

        s_blue_layer = Image.new("RGBA", (CW, CH), (0,0,0,0))
        s_blue_layer.paste(sparkle_blue, (180, 20), sparkle_blue)
        s_blue_rot = rotate_about_point(s_blue_layer, frame_idx * 6, 220, 60, scale=(s_blue_scale, s_blue_scale))

        s_pink1_layer = Image.new("RGBA", (CW, CH), (0,0,0,0))
        s_pink1_layer.paste(sparkle_pink, (120, 310), sparkle_pink)
        s_pink1_rot = rotate_about_point(s_pink1_layer, -frame_idx * 7, 155, 350, scale=(s_pink1_scale, s_pink1_scale))

        s_pink2_layer = Image.new("RGBA", (CW, CH), (0,0,0,0))
        s_pink2_layer.paste(sparkle_pink, (660, 460), sparkle_pink)
        s_pink2_rot = rotate_about_point(s_pink2_layer, frame_idx * 8, 700, 500, scale=(s_pink2_scale, s_pink2_scale), offset=(0, int(body_y * 0.5)))

        # Composite scene (back to front)
        frame = Image.new("RGBA", (CW, CH), (0,0,0,0))
        frame.paste(s_pink2_rot, (0,0), s_pink2_rot)
        frame.paste(leg_r_rot, (0,0), leg_r_rot)
        frame.paste(leg_l_rot, (0,0), leg_l_rot)
        frame.paste(body_rot, (0,0), body_rot)
        frame.paste(arm_l_rot, (0,0), arm_l_rot)
        frame.paste(arm_r_rot, (0,0), arm_r_rot)
        frame.paste(s_blue_rot, (0,0), s_blue_rot)
        frame.paste(s_pink1_rot, (0,0), s_pink1_rot)

        # Scale to optimal crisp size (e.g. 640x640)
        target_size = (640, 640)
        resized = frame.resize(target_size, resample=Image.Resampling.LANCZOS)
        frames.append(resized)

    print(f"Rendered {len(frames)} pristine frames!")

    # Save animated GIF with clean matte for #FCD8DA (site pink bg)
    gif_frames = []
    for f in frames:
        alpha = f.split()[3]
        # Clean alpha threshold
        mask = Image.eval(alpha, lambda a: 255 if a > 80 else 0)
        
        # Blend onto site header background color (#FCD8DA -> RGB: 252, 216, 218) for zero halo edges
        bg = Image.new("RGB", f.size, (252, 216, 218))
        bg.paste(f, mask=alpha)
        
        p = bg.convert("P", palette=Image.Palette.ADAPTIVE, colors=255)
        p.paste(255, ImageChops.invert(mask))
        p.info["transparency"] = 255
        gif_frames.append(p)

    out_gif = "/Users/user/.gemini/antigravity/scratch/kid_dental_2/static/images/mascot-main-2.gif"
    out_video_gif = "/Users/user/.gemini/antigravity/scratch/kid_dental_2/static/images/mascot-video.gif"
    out_tooth_gif = "/Users/user/.gemini/antigravity/scratch/kid_dental_2/static/images/mascot-tooth.gif"

    gif_frames[0].save(
        out_gif,
        save_all=True,
        append_images=gif_frames[1:],
        duration=45, # ~22 fps, 1.25s loop
        loop=0,
        disposal=2,
        transparency=255
    )
    gif_frames[0].save(
        out_video_gif,
        save_all=True,
        append_images=gif_frames[1:],
        duration=45,
        loop=0,
        disposal=2,
        transparency=255
    )
    gif_frames[0].save(
        out_tooth_gif,
        save_all=True,
        append_images=gif_frames[1:],
        duration=45,
        loop=0,
        disposal=2,
        transparency=255
    )

    print("Successfully generated ultra-smooth rigged mascot GIF!")

if __name__ == "__main__":
    main()
