import cv2
import os
import numpy as np

# Set the root directory of the project as the working directory
root_dir = os.path.dirname(os.path.abspath(__file__))  # Get the directory of the current script
project_root_dir = os.path.join(root_dir, '..')  # Get the parent directory (root directory of the project)
os.chdir(project_root_dir)  # Change to the root directory of the project

# Global variables
points = []
image_path = os.path.join(project_root_dir, 'character', 'character.png')
images_saved = False


def click_event(event, x, y, flags, param):
    global points

    # If left mouse button clicked
    if event == cv2.EVENT_LBUTTONDOWN:
        points.append((x, y))
        temp_img = img.copy()
        for point in points:
            cv2.circle(temp_img, point, 5, (0, 0, 255), -1)
        cv2.imshow('image', temp_img)

        if len(points) == 4:
            cut_and_save_mouth()

def save_with_suffix(filename, data):
    """Attempt to save the file, and if it exists, append a suffix until an available filename is found."""
    base_name, ext = os.path.splitext(filename)
    counter = 2
    while os.path.exists(os.path.join(project_root_dir, 'character', filename)):
        filename = f"{base_name}_{counter}{ext}"
        counter += 1
    cv2.imwrite(os.path.join(project_root_dir, 'character', filename), data)

def cut_and_save_mouth():
    global points, images_saved

    # Sort points for rectangle creation
    points = sorted(points, key=lambda x: x[1])

    top_left = min(points[:2], key=lambda x: x[0])
    top_right = max(points[:2], key=lambda x: x[0])
    bottom_left = min(points[2:], key=lambda x: x[0])
    bottom_right = max(points[2:], key=lambda x: x[0])

    # Cut out the mouth
    mouth = img[top_left[1]:bottom_left[1], top_left[0]:top_right[0]]

    # Create an empty transparent image with the same dimensions as the main image
    transparent_mouth_img = np.zeros_like(img)
    transparent_mouth_img[top_left[1]:bottom_left[1], top_left[0]:top_right[0]] = mouth

    save_with_suffix('mouth_same_dim.png', transparent_mouth_img)

    # Make the mouth area transparent in the original image by setting the alpha channel to 0
    img[top_left[1]:bottom_left[1], top_left[0]:top_right[0], 3] = 0
    save_with_suffix('character_without_mouth.png', img)

    # Set the flag to indicate that the images have been saved
    images_saved = True


# Read the image with alpha channel
img = cv2.imread(image_path, cv2.IMREAD_UNCHANGED)
if img.shape[2] == 3:  # If no alpha channel, add one
    img = cv2.cvtColor(img, cv2.COLOR_BGR2BGRA)

# Display the window
cv2.imshow('image', img)

# Set mouse callback function for window
cv2.setMouseCallback('image', click_event)

# Modify the key wait section to check the flag and close the window gracefully
while True:
    key = cv2.waitKey(1) & 0xFF
    if key == 27 or images_saved:  # Exit on 'ESC' key or after images have been saved
        cv2.destroyAllWindows()
        break
