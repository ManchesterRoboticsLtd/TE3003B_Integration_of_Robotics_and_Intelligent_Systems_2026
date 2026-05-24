import numpy as np
import cv2

# === [1] Initialize Camera ===

# Open the default camera (device index 0)
cam = cv2.VideoCapture(0)

# Create a named window to display the live camera feed
cv2.namedWindow("capture")

# Counter to keep track of saved images
img_counter = 0

# === [2] Main Loop: Capture, Display, and Save Frames ===

while True:
    # Read a frame from the camera
    ret, frame = cam.read()

    # If the frame wasn't captured correctly, exit the loop
    if not ret:
        print("⚠️ Failed to grab frame")
        break

    # Display the frame in the window
    cv2.imshow("capture", frame)

    # Wait for a key press (1ms)
    key = cv2.waitKey(1)

    if key % 256 == 27:
        # ESC key pressed: Exit the loop
        print("🔚 ESC pressed, closing...")
        break

    elif key % 256 == 32:
        # SPACE key pressed: Save the current frame as an image
        img_name = f"images/chess{img_counter}.png"
        cv2.imwrite(img_name, frame)
        print(f"📸 Saved: {img_name}")
        img_counter += 1

# === [3] Cleanup ===

# Release the camera and close all OpenCV windows
cam.release()
cv2.destroyAllWindows()