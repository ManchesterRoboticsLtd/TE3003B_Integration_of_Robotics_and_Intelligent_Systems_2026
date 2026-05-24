import numpy as np
import cv2 as cv
from cv2 import aruco
import yaml
from yaml.loader import SafeLoader

# === [1] Setup and Configuration ===

# Open camera device (adjust index if needed)
cam = cv.VideoCapture(2)

# Load camera calibration data from YAML file
with open('calibration_matrix.yaml') as f:
    data = yaml.load(f, Loader=SafeLoader)
    print("Loaded Camera Matrix:\n", np.array(data['camera_matrix']))

# Calibration parameters
K = np.array(data['camera_matrix'])  # Camera matrix
D = np.array(data['dist_coeff'])     # Distortion coefficients

# Define the real-world length of the marker’s side (in meters)
markerLength = 0.06  # 6 cm

# Set up ArUco dictionary and detector
dictionary = aruco.getPredefinedDictionary(aruco.DICT_4X4_50)
parameters = aruco.DetectorParameters()
detector = aruco.ArucoDetector(dictionary, parameters)

# === [2] Main Loop: Marker Detection and Pose Estimation ===

while True:
    # Capture frame from the camera
    ret, img = cam.read()
    if not ret:
        print("❌ Failed to grab frame")
        break

    # Convert image to grayscale
    gray = cv.cvtColor(img, cv.COLOR_BGR2GRAY)

    # Detect ArUco markers
    markerCorners, markerIds, rejectedCandidates = detector.detectMarkers(gray)

    if len(markerCorners) > 0:
        for i in range(len(markerIds)):
            # Estimate pose of each marker
            rvec, tvec = aruco.estimatePoseSingleMarkers(markerCorners[i], markerLength, K, D)[:2]

            # Compute distance from camera to marker
            distance = np.linalg.norm(tvec[0][0])

            # Calculate marker center in image
            corners = markerCorners[i].reshape((4, 2))
            topLeft, topRight, bottomRight, bottomLeft = corners
            cX = int((topLeft[0] + bottomRight[0]) / 2.0)
            cY = int((topLeft[1] + bottomRight[1]) / 2.0)

            # Draw marker and its pose axis
            aruco.drawDetectedMarkers(img, markerCorners, markerIds)
            cv.drawFrameAxes(img, K, D, rvec, tvec, 0.01)

            # Annotate distance on image
            cv.putText(img, f"{distance:.2f} m", (cX, cY - 15),
                       cv.FONT_HERSHEY_SIMPLEX, 0.4, (0, 255, 0), 2)

    # Display result
    cv.imshow("capture", img)

    # Break loop if ESC is pressed
    k = cv.waitKey(1)
    if k % 256 == 27:
        print("🔚 ESC pressed, closing...")
        break

# === [3] Cleanup ===

cam.release()
cv.destroyAllWindows()