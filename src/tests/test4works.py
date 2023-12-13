from moviepy.editor import VideoFileClip, CompositeVideoClip
from moviepy.video.fx.mask_color import mask_color

import cv2
import numpy as np


def overlay_clips(fg_path, bg_path, output_path):
    def remove_green_background(frame):
        # Create a mask for the circular region inside the specified circle
        hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
        lower_green = np.array([40, 40, 40])
        upper_green = np.array([80, 255, 255])
        mask = cv2.inRange(hsv, lower_green, upper_green)

        # Create a circular mask with a specified radius and center
        h, w = frame.shape[:2]
        center = (200, 200)
        radius = 190
        rr, cc = np.ogrid[:h, :w]
        circle_mask = (rr - center[0])**2 + (cc - center[1])**2 <= radius**2

        # Set pixels inside the circle to 255 (white) and outside to 0 (black)
        mask[~circle_mask] = 0

        # Apply the mask to the frame
        result_frame = cv2.bitwise_and(frame, frame, mask=mask)

        return result_frame

    # Load foreground and background clips
    fg_clip = VideoFileClip(fg_path)
    bg_clip = VideoFileClip(bg_path)
    min_duration = bg_clip.duration
    fg_clip = fg_clip.subclip(0, min_duration)

    # Initialize transparent foreground clip
    transparent_fg_clip = fg_clip.fl_image(lambda img: remove_green_background(img))

    transparent_fg_clip = mask_color(transparent_fg_clip, color=[0, 0, 0], thr=1)
    # Overlay clips
    final_clip = CompositeVideoClip(
        [bg_clip, transparent_fg_clip.set_position(("left", "bottom"))], size=bg_clip.size
    )

    # Apply mask_color to set black pixels to transparent

    # Write output video
    final_clip.write_videofile(output_path, codec="libx264", audio_codec="aac", fps=60)

fg_path = "data/inputs/circle with green.mp4"
bg_path = "data/inputs/3gi.co.uk_bk30.mp4"
output_path = "final2.mp4"

overlay_clips(fg_path, bg_path, output_path)
