# import numpy as np
# from moviepy.editor import VideoFileClip

# def round_mask(size, radius):
#     h, w = size
#     mask = np.zeros((h, w), dtype=np.uint8)
#     center = (h // 2, w // 2)
#     rr, cc = np.ogrid[:h, :w]
#     mask[(rr - center[0])**2 + (cc - center[1])**2 <= radius**2] = 1
#     return mask

# def crop_with_rounded_mask(clip, radius=400):
#     mask = round_mask(clip.size, radius)
#     return clip.fl_image(lambda pic: np.multiply(pic, mask[:, :, None]), apply_to=["mask"])

# # Load the video clip
# clip = VideoFileClip("data/inputs/KD 30.mp4")

# # Crop the video with a rounded mask at the center
# cropped_clip = crop_with_rounded_mask(clip, radius=400)

# # Display or save the resulting video
# cropped_clip.write_videofile("output.mp4")

import numpy as np
from moviepy.editor import VideoFileClip, ImageSequenceClip


def round_mask(size, radius):
    h, w = size
    mask = np.zeros((h, w), dtype=np.uint8)
    center = (h // 2, w // 2)
    rr, cc = np.ogrid[:h, :w]
    mask[(rr - center[0])**2 + (cc - center[1])**2 <= radius**2] = 255
    return mask


def crop_with_rounded_mask(clip, radius=400):
    mask = round_mask(clip.size, radius)
    mask = np.stack([mask] * 3, axis=-1)  # Create a 3-channel mask for RGB images
    mask_normalized = mask / 255.0  # Normalize to values between 0 and 1

    return clip.fl_image(lambda pic: pic * mask_normalized, apply_to=["mask"])


# Load the video clip
clip = VideoFileClip("data/inputs/KD 30.mp4")

# Crop the video with a rounded mask and make the outside transparent
cropped_clip = crop_with_rounded_mask(clip, radius=400)

# Display or save the resulting video
cropped_clip.write_videofile("output_t.mp4", codec="libx264", audio_codec="aac")
