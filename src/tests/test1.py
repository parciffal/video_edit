from moviepy.editor import CompositeVideoClip, VideoFileClip
import numpy as np

def round_mask(size, radius):
    h, w = size
    mask = np.zeros((h, w), dtype=np.uint8)
    center = (h // 2, w // 2)
    rr, cc = np.ogrid[:h, :w]
    mask[(rr - center[0])**2 + (cc - center[1])**2 <= radius**2] = 255
    return mask

def make_black_transparent(frame, radius):
    # Create a circular mask
    mask = round_mask(frame.shape[:2], radius)
    mask = np.stack([mask] * 3, axis=-1)  # Create a 3-channel mask for RGB images
    mask_normalized = mask / 255.0  # Normalize to values between 0 and 1

    # Apply the circular mask to the frame
    frame *= mask_normalized

    # Convert the frame to grayscale
    gray_frame = np.mean(frame, axis=-1)

    # Create a mask for black pixels
    black_mask = (gray_frame == 0)

    # Create an alpha channel
    alpha_channel = np.ones_like(gray_frame) * 255
    alpha_channel[black_mask] = 0

    # Add the alpha channel to the frame
    frame_with_alpha = np.concatenate([frame, alpha_channel[..., None]], axis=-1)

    return frame_with_alpha.astype(np.uint8)

def apply_black_transparency(clip, th, radius):
    return clip.fl_image(lambda pic: make_black_transparent(pic, radius), apply_to=["mask"])


# Load video clips
clib_background = VideoFileClip("data/inputs/3gi.co.uk_bk30.mp4")
clip_loom = VideoFileClip("data/inputs/bk 30.mp4")

# Ensure both clips have the same duration
min_duration = min(clib_background.duration, clip_loom.duration)
clib_background = clib_background.subclip(0, min_duration)
clip_loom = clip_loom.subclip(0, min_duration)

# Set the radius for the circular mask
radius = 400

# Apply black transparency to clip_loom
clip_loom = apply_black_transparency(clip_loom, 6, radius)

min_size = clib_background.size

final_clip = CompositeVideoClip(
    [clib_background.set_duration(min_duration), clip_loom.set_position(("left", "bottom"))],
    size=min_size
)

final_clip.write_videofile("data/outputs/3gi.co.uk_bk30.mp4", codec="libx264", audio_codec="aac")
