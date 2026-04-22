import os
from launch import LaunchDescription
from launch_ros.actions import Node
from ament_index_python.packages import get_package_share_directory

def generate_launch_description():
    urdf_file_name = 'puzzle_drone.urdf'
    urdf_path = os.path.join(
        get_package_share_directory('puzzle_drone'),
        'urdf',
        urdf_file_name)
    
    with open(urdf_path, 'r') as infp:
        robot_desc = infp.read()



    
    return LaunchDescription([])