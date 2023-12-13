from moviepy.editor import VideoFileClip, CompositeVideoClip
import os
# from moviepy.video.fx.mask_color import mask_color

# import cv2
import numpy as np


def mask_color(clip, color=None, radius=None, center=(200, 200)):
    if color is None:
        color = [0, 0, 0]
    color = np.array(color)

    if radius is None:
        radius = 190
    center = np.array(center)

    def add_circle_mask(frame):
        h, w = frame.shape[:2]

        Y, X = np.ogrid[:h, :w]
        circle_mask = (X - center[0]) ** 2 + (Y - center[1]) ** 2 <= radius**2
        return circle_mask.astype(np.uint8) * 255

    def hill(x):
        return 1.0 * (x != 0)

    def flim(im):
        if radius is None:
            return hill(np.sqrt(((im - color) ** 2).sum(axis=2)))
        else:
            return hill(add_circle_mask(im))

    mask = clip.fl_image(flim)
    mask.ismask = True

    new_clip = clip.set_mask(mask)
    return new_clip


def overlay_clips(bg_path, output_path, video_path):
    # Load foreground and background clips
    fg_clip = VideoFileClip(fg_path)

    # Initialize transparent foreground clip
    transparent_fg_clip = mask_color(fg_clip, color=[0, 0, 0], radius=188)

    # Overlay clips
    files = os.listdir(video_path)
    for video in files:
        file_path = os.path.join(video_path, video)
        try:
            # Check if the file is a video file (you may need to modify the list of video extensions)
            if os.path.isfile(file_path) and file_path.lower().endswith(('.mp4', '.avi', '.mkv', '.mov')):
                bg_clip = VideoFileClip(bg_path)
                min_duration = bg_clip.duration
                transparent_fg_clip.subclip(0, min_duration)

                final_clip = CompositeVideoClip(
                    [bg_clip, transparent_fg_clip.set_position(("left", "bottom"))],
                    size=bg_clip.size,
                )

                # Apply mask_color to set black pixels to transparent

                # Write output video
                out_path = file_path = os.path.join(output_path, video)
                final_clip.write_videofile(out_path, codec="libx264", audio_codec="aac", fps=60)
        except Exception as e:
            print(e)
            continue


fg_path = "data/inputs/circle with green.mp4"
output_path = "data/outputs/"
video_path = "data/videos/"

overlay_clips(fg_path, video_path, output_path)
