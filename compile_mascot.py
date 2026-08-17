import os
import subprocess
import shutil
from PIL import Image

def main():
    frames_dir = "/Users/user/.gemini/antigravity/scratch/kid_dental_2/temp_frames"
    out_gif = "/Users/user/.gemini/antigravity/scratch/kid_dental_2/static/images/mascot-main-2.gif"
    out_png = "/Users/user/.gemini/antigravity/scratch/kid_dental_2/static/images/mascot-main-2.png"
    out_tooth = "/Users/user/.gemini/antigravity/scratch/kid_dental_2/static/images/mascot-tooth.png"

    # 1. Generate APNG (Animated PNG) via Pillow (Lossless 32-bit RGBA, 30 fps)
    frame_files = sorted([f for f in os.listdir(frames_dir) if f.startswith("frame_") and f.endswith(".png")])
    pil_frames = [Image.open(os.path.join(frames_dir, f)).convert("RGBA") for f in frame_files]

    pil_frames[0].save(
        out_png,
        save_all=True,
        append_images=pil_frames[1:],
        duration=33, # 33ms per frame = 30 fps
        loop=0,
        disposal=2
    )
    shutil.copy(out_png, out_tooth)
    print("Saved lossless animated APNG (mascot-main-2.png) at 30 fps!")

    # 2. Generate animated GIF via FFmpeg
    gif_cmd = [
        "/opt/homebrew/bin/ffmpeg", "-y",
        "-framerate", "30",
        "-i", f"{frames_dir}/frame_%03d.png",
        "-filter_complex", "[0:v] split [a][b];[a] palettegen=reserve_transparent=on:stats_mode=full [p];[b][p] paletteuse=dither=none:alpha_threshold=128",
        out_gif
    ]
    subprocess.run(gif_cmd, check=True)
    shutil.copy(out_gif, "/Users/user/.gemini/antigravity/scratch/kid_dental_2/static/images/mascot-video.gif")
    shutil.copy(out_gif, "/Users/user/.gemini/antigravity/scratch/kid_dental_2/static/images/mascot-tooth.gif")
    print("Generated high-quality GIF (mascot-main-2.gif) successfully!")

if __name__ == "__main__":
    main()
