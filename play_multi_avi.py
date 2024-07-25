import cv2
import numpy as np
import os

def get_video_paths(directory, extension='.avi'):
    video_paths = []
    for root, dirs, files in os.walk(directory):
        for file in files:
            if file.endswith(extension):
                video_paths.append(os.path.join(root, file))
    return video_paths

# Specify the directory
directory = '/Users/cainan/Downloads/output/box_test_rate30'
# directory = '/Users/cainan/Downloads/output/box_test_rate10'
directory = '/Users/cainan/Downloads/output/box_test_rate5'

# Get all .avi files in the directory
video_paths = get_video_paths(directory)

# Print the paths
for path in video_paths:
    print(path)

caps = [cv2.VideoCapture(video_path) for video_path in video_paths]

# Check if the videos were opened successfully
for i, cap in enumerate(caps):
    if not cap.isOpened():
        print(f"Error: Could not open video {i}.")
        exit()

# Get the frame size of the first video
frame_width = int(caps[0].get(cv2.CAP_PROP_FRAME_WIDTH))
frame_height = int(caps[0].get(cv2.CAP_PROP_FRAME_HEIGHT))
blank_frame = np.zeros((frame_height, frame_width, 3), dtype=np.uint8)

# Read and display the video frames
while True:
    frames = []
    all_rets_false = True  # Flag to check if all ret values are False
    for i, cap in enumerate(caps):
        ret, frame = cap.read()

        # If we got frames, resize them to the first video's frame size
        if ret:
            frame = cv2.resize(frame, (frame_width, frame_height))
            frames.append(frame)
            all_rets_false = False  # At least one frame is valid
        else:
            frames.append(blank_frame)

    # Concatenate frames horizontally
    combined_frame = np.hstack(frames)

    # Display the combined frame
    cv2.imshow(directory, combined_frame)

    # Break the loop if all ret values are False
    if all_rets_false:
        break

    # Press 'q' on the keyboard to exit the loop
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release the video capture objects and close all OpenCV windows
for cap in caps:
    cap.release()
cv2.destroyAllWindows()
