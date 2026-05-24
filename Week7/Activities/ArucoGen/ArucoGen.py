import cv2
from cv2 import aruco
import os

# Save location
dir_mark = r'C:\Users\mario\OneDrive - Manchester Robotics Limited\Test\Aruco_Markers'

# Parameter
num_mark = 10 #Number of markers
size_mark = 250 #Size of markers in pixels

### --- marker images are generated and saved --- ###
# Call marker type
dict_aruco = cv2.aruco.getPredefinedDictionary(cv2.aruco.DICT_4X4_250)
print(dict_aruco)

for count in range(num_mark) :

    id_mark = count
    img_mark = cv2.aruco.generateImageMarker(dict_aruco, id_mark, size_mark)

    if count < 10 :
        img_name_mark = 'mark_id_0' + str(count) + '.jpg'
    else :
        img_name_mark = 'mark_id_' + str(count) + '.jpg'

    path_mark = os.path.join(dir_mark, img_name_mark)

    cv2.imwrite(path_mark, img_mark)