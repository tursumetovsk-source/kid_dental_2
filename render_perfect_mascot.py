import os
import math
import subprocess
import shutil
from PIL import Image

def rotate_about_pivot(img, angle_deg, pivot_x, pivot_y, canvas_size=(800, 800), offset=(0, 0), scale=(1.0, 1.0)):
    CW, CH = canvas_size
    cx, cy = CW // 2, CH // 2
    dx = cx - pivot_x
    dy = cy - pivot_y

    layer = Image.new("RGBA", (CW, CH), (0,0,0,0))
    layer.paste(img, (int(dx), int(dy)), img)

    if scale != (1.0, 1.0):
        sw = max(1, int(CW * scale[0]))
        sh = max(1, int(CH * scale[1]))
        scaled = layer.resize((sw, sh), resample=Image.Resampling.LANCZOS)
        layer = Image.new("RGBA", (CW, CH), (0,0,0,0))
        layer.paste(scaled, ((CW - sw)//2, (CH - sh)//2), scaled)

    rotated = layer.rotate(angle_deg, resample=Image.Resampling.BICUBIC)

    final_canvas = Image.new("RGBA", (CW, CH), (0,0,0,0))
    fx = -dx + offset[0]
    fy = -dy + offset[1]
    final_canvas.paste(rotated, (int(fx), int(fy)), rotated)
    return final_canvas

def main():
    parts_dir = "/Users/user/.gemini/antigravity/scratch/kid_dental_2/static/images/mascot_parts"
    frames_dir = "/Users/user/.gemini/antigravity/scratch/kid_dental_2/temp_frames"
    os.makedirs(frames_dir, exist_ok=True)

    # Clean old frames
    for f in os.listdir(frames_dir):
        if f.endswith(".png"):
            os.remove(os.path.join(frames_dir, f))

    # Load high-res parts
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

    CW, CH = 800, 800
    # Center character nicely in 800x800
    # In test_assembly: canvas was 900x900 with offset (50, 50)
    # We map 900x900 -> 800x800 by shifting -50, -50
    OX, OY = -50, -50

    num_frames = 36 # 36 frames at 30 fps = 1.2s silky smooth loop

    for frame_idx in range(num_frames):
        t = frame_idx / num_frames
        phase = t * 2 * math.pi

        # 1. Rhythmic Body Bobbing (2 smooth beats per loop)
        body_y = math.sin(phase * 2) * 10.0
        body_squash = 1.0 + math.sin(phase * 2) * 0.02
        body_stretch = 1.0 - math.sin(phase * 2) * 0.015
        body_tilt = math.sin(phase) * 2.0

        # 2. Left Arm (Peace sign wave)
        # Shoulder joint at (190, 310) in 800x800
        arm_l_angle = math.sin(phase) * 10.0
        arm_l_layer = Image.new("RGBA", (CW, CH), (0,0,0,0))
        arm_l_layer.paste(arm_left_full, (50 + OX, 60 + OY), arm_left_full)
        arm_l_rot = rotate_about_pivot(
            arm_l_layer,
            arm_l_angle,
            pivot_x=190,
            pivot_y=310,
            offset=(0, int(body_y))
        )

        # 3. Right Arm (Bottle pump)
        # Shoulder joint at (520, 320)
        arm_r_angle = -math.sin(phase) * 9.0
        arm_r_layer = Image.new("RGBA", (CW, CH), (0,0,0,0))
        arm_r_layer.paste(arm_right_full, (540 + OX, 60 + OY), arm_right_full)
        arm_r_rot = rotate_about_pivot(
            arm_r_layer,
            arm_r_angle,
            pivot_x=520,
            pivot_y=320,
            offset=(0, int(body_y))
        )

        # 4. Left Leg (Front sneaker bounce)
        # Hip anchor at (230, 450)
        leg_l_angle = math.sin(phase) * 6.0
        leg_l_layer = Image.new("RGBA", (CW, CH), (0,0,0,0))
        leg_l_layer.paste(leg_l, (70 + OX, 420 + OY), leg_l)
        leg_l_rot = rotate_about_pivot(
            leg_l_layer,
            leg_l_angle,
            pivot_x=230,
            pivot_y=450,
            offset=(0, int(body_y * 0.5))
        )

        # 5. Right Leg (Back sneaker flex)
        # Hip anchor at (430, 470)
        leg_r_angle = -math.sin(phase) * 5.0
        leg_r_layer = Image.new("RGBA", (CW, CH), (0,0,0,0))
        leg_r_layer.paste(leg_r, (360 + OX, 430 + OY), leg_r)
        leg_r_rot = rotate_about_pivot(
            leg_r_layer,
            leg_r_angle,
            pivot_x=430,
            pivot_y=470,
            offset=(0, int(body_y * 0.5))
        )

        # 6. Body + Face
        body_canvas = Image.new("RGBA", (CW, CH), (0,0,0,0))
        body_canvas.paste(body, (220 + OX, 120 + OY), body)
        
        mouth_y = int(320 + OY + math.sin(phase * 2) * 2)
        body_canvas.paste(mouth, (390 + OX, mouth_y), mouth)

        glasses_y = int(185 + OY + math.sin(phase * 2) * 1)
        body_canvas.paste(glasses, (260 + OX, glasses_y), glasses)

        eyebrow_y = int(125 + OY + math.sin(phase * 2) * 2.5)
        body_canvas.paste(eyebrow_l, (320 + OX, eyebrow_y), eyebrow_l)
        body_canvas.paste(eyebrow_r, (490 + OX, eyebrow_y - 4), eyebrow_r)

        body_rot = rotate_about_pivot(
            body_canvas,
            body_tilt,
            pivot_x=400,
            pivot_y=300,
            offset=(0, int(body_y)),
            scale=(body_stretch, body_squash)
        )

        # 7. Sparkles
        s_blue_scale = 1.0 + math.sin(phase * 2) * 0.2
        s_pink1_scale = 1.0 + math.cos(phase * 2 + 1) * 0.25
        s_pink2_scale = 1.0 + math.sin(phase * 2 + 2) * 0.2

        s_blue_layer = Image.new("RGBA", (CW, CH), (0,0,0,0))
        s_blue_layer.paste(sparkle_blue, (180 + OX, 20 + OY), sparkle_blue)
        s_blue_rot = rotate_about_pivot(s_blue_layer, frame_idx * 10, 170, 10, scale=(s_blue_scale, s_blue_scale))

        s_pink1_layer = Image.new("RGBA", (CW, CH), (0,0,0,0))
        s_pink1_layer.paste(sparkle_pink, (120 + OX, 310 + OY), sparkle_pink)
        s_pink1_rot = rotate_about_pivot(s_pink1_layer, -frame_idx * 10, 105, 300, scale=(s_pink1_scale, s_pink1_scale))

        s_pink2_layer = Image.new("RGBA", (CW, CH), (0,0,0,0))
        s_pink2_layer.paste(sparkle_pink, (660 + OX, 460 + OY), sparkle_pink)
        s_pink2_rot = rotate_about_pivot(s_pink2_layer, frame_idx * 10, 650, 450, scale=(s_pink2_scale, s_pink2_scale), offset=(0, int(body_y * 0.4)))

        # Composite scene
        frame = Image.new("RGBA", (CW, CH), (0,0,0,0))
        frame.paste(s_pink2_rot, (0,0), s_pink2_rot)
        frame.paste(leg_r_rot, (0,0), leg_r_rot)
        frame.paste(leg_l_rot, (0,0), leg_l_rot)
        frame.paste(body_rot, (0,0), body_rot)
        frame.paste(arm_l_rot, (0,0), arm_l_rot)
        frame.paste(arm_r_rot, (0,0), arm_r_rot)
        frame.paste(s_blue_rot, (0,0), s_blue_rot)
        frame.paste(s_pink1_rot, (0,0), s_pink1_rot)

        frame_path = os.path.join(frames_dir, f"frame_{frame_idx:03d}.png")
        frame.save(frame_path)

    print(f"Saved {num_frames} pristine frames to {frames_dir}!")

    # Use FFmpeg with optimal palette generation for true crystal clear transparency and rich colors
    out_gif = "/Users/user/.gemini/antigravity/scratch/kid_dental_2/static/images/mascot-main-2.gif"
    out_video_gif = "/Users/user/.gemini/antigravity/scratch/kid_dental_2/static/images/mascot-video.gif"
    out_tooth_gif = "/Users/user/.gemini/antigravity/scratch/kid_dental_2/static/images/mascot-tooth.gif"

    palette_cmd = [
        "/opt/homebrew/bin/ffmpeg", "-y",
        "-framerate", "30",
        "-i", f"{frames_dir}/frame_%03d.png",
        "-vf", "palettegen=reserve_transparent=1:stats_mode=single",
        f"{frames_dir}/palette.png"
    ]
    subprocess.run(palette_cmd, check=True)

    gif_cmd = [
        "/opt/homebrew/bin/ffmpeg", "-y",
        "-framerate", "30",
        "-i", f"{frames_dir}/frame_%03d.png",
        "-i", f"{frames_dir}/palette.png",
        "-lavfi", "paletteuse=alpha_threshold=128:dither=none",
        out_gif
    ]
    subprocess.run(gif_cmd, check=True)

    shutil.copy(out_gif, out_video_gif)
    shutil.copy(out_gif, out_tooth_gif)
    print("FFmpeg generated ultra-crisp transparent GIF successfully at 30 fps!")

if __name__ == "__main__":
    main()
