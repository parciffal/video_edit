import cv2
import numpy as np
from moviepy.editor import VideoFileClip, ImageSequenceClip

# Load the video clip
clip = VideoFileClip("data/inputs/bk 30.mp4")

# Get the video parameters
width = int(clip.size[0])
height = int(clip.size[1])

# Create a circular mask
mask = np.zeros((height, width), dtype=np.uint8)
center = (width // 2, height // 2)
radius = min(width, height) // 3
cv2.circle(mask, center, radius, (255), thickness=-1)

# Convert the VideoClip to a NumPy array
video_array = np.array(list(clip.iter_frames()))

# Apply the circular mask to each frame
masked_video = []
for frame in video_array:
    masked_frame = cv2.bitwise_and(frame, frame, mask=mask)
    masked_video.append(masked_frame)

# Convert the list of masked frames back to a NumPy array
masked_video_array = np.array(masked_video)

# Convert the NumPy array back to a VideoClip
masked_clip = ImageSequenceClip(list(masked_video_array), fps=clip.fps)

# Display or save the resulting video
masked_clip.write_videofile("output_with_circular_mask.mp4", codec="libx264", audio_codec="aac")
