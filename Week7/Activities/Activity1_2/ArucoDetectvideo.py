import cv2 as cv
from cv2 import aruco

cam = cv.VideoCapture(2)

markerLength = 0.09

aruco_type = "DICT_4X4_250"

dictionary = cv.aruco.getPredefinedDictionary(cv.aruco.DICT_4X4_50)
parameters =  cv.aruco.DetectorParameters()
detector = cv.aruco.ArucoDetector(dictionary, parameters)

while True:

    ret, img = cam.read()
    if not ret:
        print("failed to grab frame")
        break

    markerCorners, markerIds, rejectedCandidates = detector.detectMarkers(img)

    # verify *at least* one ArUco marker was detected
    if len(markerCorners) > 0:
        cv.aruco.drawDetectedMarkers(img,markerCorners,markerIds)

        # flatten the ArUco IDs list
        ids = markerIds.flatten()
        # loop over the detected ArUCo corners
        for (markerCorner, markerID) in zip(markerCorners, ids):
            # extract the marker corners (which are always returned in
            # top-left, top-right, bottom-right, and bottom-left order)
            corners = markerCorner.reshape((4, 2))

            (topLeft, topRight, bottomRight, bottomLeft) = corners
            # convert each of the (x, y)-coordinate pairs to integers
            topRight = (int(topRight[0]), int(topRight[1]))
            bottomRight = (int(bottomRight[0]), int(bottomRight[1]))
            bottomLeft = (int(bottomLeft[0]), int(bottomLeft[1]))
            topLeft = (int(topLeft[0]), int(topLeft[1]))
            
            # compute and draw the center (x, y)-coordinates of the ArUco
            # marker
            cX = int((topLeft[0] + bottomRight[0]) / 2.0)
            cY = int((topLeft[1] + bottomRight[1]) / 2.0)
            cv.circle(img, (cX, cY), 4, (0, 0, 255), -1)
           
            
    cv.imshow("capture", img)

    k = cv.waitKey(1)
    if k%256 == 27:
        # ESC pressed
        print("Escape hit, closing...")
        break

cam.release()
cv.destroyAllWindows()

