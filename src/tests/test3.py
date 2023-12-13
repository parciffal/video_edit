import cv2
import numpy as np

# Function to create a circular mask
def create_circle_mask(height, width, center, radius):
    mask = np.zeros((height, width), dtype=np.uint8)
    cv2.circle(mask, center, radius, (255, 255, 255), thickness=cv2.FILLED)
    return mask

# Read the outlying clip
outlying_clip = cv2.VideoCapture('data/inputs/bk 30.mp4')  # Replace with your outlying clip file

# Read the background clip
background_clip = cv2.VideoCapture('data/inputs/3gi.co.uk_bk30.mp4')  # Replace with your background clip file

# Get clip properties
width = int(outlying_clip.get(cv2.CAP_PROP_FRAME_WIDTH))
height = int(outlying_clip.get(cv2.CAP_PROP_FRAME_HEIGHT))
fps = outlying_clip.get(cv2.CAP_PROP_FPS)

# Create VideoWriter object to save the output
fourcc = cv2.VideoWriter_fourcc(*'mp4v')
output_video = cv2.VideoWriter('output_video.mp4', fourcc, fps, (width, height))

# Define the center and radius of the circle
center = (width // 2, height // 2)
radius = min(width, height) // 4

while True:
    ret_outlying, outlying_frame = outlying_clip.read()
    if not ret_outlying:
        break

    # Resize the outlying frame to match the background frame
    ret_bg, background_frame = background_clip.read()
    if not ret_bg:
        break
    outlying_frame = cv2.resize(outlying_frame, (width, height))

    # Create a circular mask
    mask = create_circle_mask(height, width, center, radius)

    # Make everything outside the circle transparent in the outlying frame
    outlying_frame[mask == 0] = 0

    # Replace background pixels with outlying pixels
    result_frame = outlying_frame.copy()

    # Display the frame
    cv2.imshow('Output Video', result_frame)
    output_video.write(result_frame)

    # Break the loop if 'q' is pressed
    if cv2.waitKey(30) & 0xFF == ord('q'):
        break

# Release clip capture and writer objects
outlying_clip.release()
background_clip.release()
output_video.release()

# Destroy any OpenCV windows
cv2.destroyAllWindows()