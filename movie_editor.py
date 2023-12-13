from moviepy.editor import ImageClip, VideoFileClip, CompositeVideoClip
from moviepy.video.fx.mask_color import mask_color

import cv2
import numpy as np


def overlay_clips(fg_path, bg_path, output_path):
    def remove_green_background(frame):
        # Remove green background
        hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
        lower_green = np.array([40, 40, 40])
        upper_green = np.array([80, 255, 255])
        mask = cv2.inRange(hsv, lower_green, upper_green)
        inverse_mask = cv2.bitwise_not(mask)
        transparent_frame = cv2.bitwise_and(frame, frame, mask=inverse_mask)
        return transparent_frame

    # Load foreground and background clips
    fg_clip = VideoFileClip(fg_path)
    bg_clip = VideoFileClip(bg_path)
    min_duration = bg_clip.duration
    fg_clip = fg_clip.subclip(0, min_duration)

    # Initialize transparent foreground clip
    transparent_fg_clip = fg_clip.fl_image(lambda img: remove_green_background(img))
    transparent_fg_clip1 = mask_color(transparent_fg_clip, color=(0, 0, 0), thr=1)
    min_size = bg_clip.size

    # Overlay clips
    final_clip = CompositeVideoClip(
        [bg_clip, transparent_fg_clip1.set_position(("left", "bottom"))], size=min_size
    )

    # Apply mask_color to set black pixels to transparent

    # Write output video
    final_clip.write_videofile(output_path, codec="libx264", audio_codec="aac", fps=60)


fg_path = "data/inputs/circle with green.mp4"
bg_path = "data/inputs/3gi.co.uk_bk30.mp4"
output_path = "final2.mp4"

overlay_clips(fg_path, bg_path, output_path)
