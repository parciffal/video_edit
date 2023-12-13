from moviepy.editor import VideoFileClip, CompositeVideoClip
import numpy as np
import cv2


def remove_color(image, target_color, threshold=30):
    hsv_image = cv2.cvtColor(np.array(image), cv2.COLOR_RGB2HSV)
    lower_bound = np.array([target_color[0] - threshold, 30, 30])
    upper_bound = np.array([target_color[0] + threshold, 255, 255])
    mask = cv2.inRange(hsv_image, lower_bound, upper_bound)
    image_array = np.array(image)
    image_array[mask != 0] = [0, 0, 0]
    return image_array


# Load the video clip with a green screen
green_screen_clip = VideoFileClip("data/inputs/KD 1.mp4")

# Define the target color range in HSV (green color in this case)
target_color = [60, 255, 255]

# Apply color removal
color_removed_clip = green_screen_clip.fl_image(lambda img: remove_color(img, target_color, threshold=30))

# Load a background clip (replace with your background video)
background_clip = VideoFileClip("data/inputs/3gi.co.uk_bk30.mp4")

# Combine the color-removed clip with the background clip
final_clip = CompositeVideoClip(
    [background_clip.set_duration(green_screen_clip.duration),
     color_removed_clip.set_duration(green_screen_clip.duration)],
    size=color_removed_clip.size
)

# Write the final video file
final_clip.write_videofile("output_video.mp4", codec="libx264", audio_codec="aac")