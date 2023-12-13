import cv2
import numpy as np
from moviepy.editor import VideoFileClip, CompositeVideoClip, VideoClip

def apply_mask(frame):
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    lower_green = np.array([40, 40, 40])
    upper_green = np.array([80, 255, 255])
    mask = cv2.inRange(hsv, lower_green, upper_green)
    
    # Make sure the mask has the same size as the frame
    mask = cv2.resize(mask, (frame.shape[1], frame.shape[0]))

    # Make the mask three channels for compatibility with the frame
    mask = cv2.cvtColor(mask, cv2.COLOR_GRAY2BGR)
    
    # Invert the mask (optional, depending on how you want to use it)
    mask_inv = cv2.bitwise_not(mask)
    
    # Apply the mask to the frame
    result = cv2.bitwise_and(frame, frame, mask=mask_inv)
    
    return result

def apply_mask_to_video(input_path, output_path):
    # Load video clip
    video_clip = VideoFileClip(input_path)

    # Apply the mask to each frame using the apply_mask function
    masked_frames = [apply_mask(frame) for frame in video_clip.iter_frames()]

    # Create a VideoClip from the list of masked frames
    masked_clip = VideoClip(lambda t: masked_frames[int(t * video_clip.fps)], duration=video_clip.duration)

    # Write the output video
    masked_clip.write_videofile(output_path, codec="libx264", audio_codec="aac", fps=video_clip.fps)


# Replace 'input_video.mp4' and 'output_video.mp4' with your file paths
apply_mask_to_video("data/inputs/circle with green.mp4", "output_video.mp4")
