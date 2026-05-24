import numpy as np
import cv2 as cv
import glob
import yaml

# === [1] Setup ===

# Size of the chessboard pattern (number of inner corners per chessboard row and column)
chessboard_size = (9, 6)

# Image resolution
frame_size = (640, 480)

# Termination criteria for cornerSubPix: max 30 iterations or epsilon < 0.001
criteria = (cv.TERM_CRITERIA_EPS + cv.TERM_CRITERIA_MAX_ITER, 30, 0.001)

# Prepare known object points in 3D space (0,0,0), (1,0,0), ..., (8,5,0)
objp = np.zeros((chessboard_size[0] * chessboard_size[1], 3), np.float32)
objp[:, :2] = np.mgrid[0:chessboard_size[0], 0:chessboard_size[1]].T.reshape(-1, 2)

# Arrays to store 3D object points and 2D image points from all calibration images
objpoints = []  # 3D points in real world space
imgpoints = []  # 2D points in image plane

# === [2] Load and process all chessboard images ===

images = glob.glob('images/*.png')

for fname in images:
    img = cv.imread(fname)
    gray = cv.cvtColor(img, cv.COLOR_BGR2GRAY)

    # Try to find the chessboard corners
    ret, corners = cv.findChessboardCorners(gray, chessboard_size, None)
    print(fname, "  Chessboard found:", ret)

    if ret:
        # Refine corner positions and save them
        corners2 = cv.cornerSubPix(gray, corners, (11, 11), (-1, -1), criteria)
        objpoints.append(objp)
        imgpoints.append(corners2)

        # Draw the corners on the image
        cv.drawChessboardCorners(img, chessboard_size, corners2, ret)
        cv.imshow('Chessboard', img)
        cv.waitKey(500)

cv.destroyAllWindows()

# === [3] Calibrate the camera ===

ret, camera_matrix, dist_coeffs, rvecs, tvecs = cv.calibrateCamera(
    objpoints, imgpoints, gray.shape[::-1], None, None)

print("\n=== Calibration Results ===")
print("Reprojection error:", ret)
print("\nCamera Matrix:\n", camera_matrix)
print("\nDistortion Coefficients:\n", dist_coeffs)
print("\nRotation Vectors:\n", rvecs)
print("\nTranslation Vectors:\n", tvecs)

# === [4] Undistort one of the images ===

img = cv.imread('images/chess3.png')
h, w = img.shape[:2]

# Compute the optimal new camera matrix to minimize unwanted pixels
new_camera_matrix, roi = cv.getOptimalNewCameraMatrix(camera_matrix, dist_coeffs, (w, h), 1, (w, h))

# Undistort the image
undistorted = cv.undistort(img, camera_matrix, dist_coeffs, None, new_camera_matrix)

# Crop the image using the ROI
x, y, w, h = roi
undistorted_cropped = undistorted[y:y+h, x:x+w]

# Save the undistorted image
cv.imwrite('calibresult.png', undistorted_cropped)

# === [5] Save calibration data to a YAML file ===

calibration_data = {
    'camera_matrix': camera_matrix.tolist(),
    'dist_coeff': dist_coeffs.tolist(),
    'rotation_vector': [r.tolist() for r in rvecs],
    'translation_vector': [t.tolist() for t in tvecs]
}

with open("calibration_matrix.yaml", "w") as f:
    yaml.dump(calibration_data, f)

# === [6] Calculate mean reprojection error ===

mean_error = 0
for i in range(len(objpoints)):
    projected_imgpoints, _ = cv.projectPoints(objpoints[i], rvecs[i], tvecs[i], camera_matrix, dist_coeffs)
    error = cv.norm(imgpoints[i], projected_imgpoints, cv.NORM_L2) / len(projected_imgpoints)
    mean_error += error

print("\nMean reprojection error: {:.4f}".format(mean_error / len(objpoints)))