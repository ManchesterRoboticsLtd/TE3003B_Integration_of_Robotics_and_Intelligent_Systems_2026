#IMPORTS REQUIRED TO SET THE PACKAGE ADDRESS (DIRECTORIES)
import os
from ament_index_python.packages import get_package_share_directory

#IMPORTS REQUIRED FOR Launching Nodes
from launch import LaunchDescription
from launch_ros.actions import Node
from launch_ros.parameter_descriptions import ParameterValue

#IMPORTS REQUIRED FOR EVENTS AND ACTIONS
from launch.actions import  EmitEvent, LogInfo, RegisterEventHandler
from launch.event_handlers import OnProcessExit
from launch.events import Shutdown
from launch.substitutions import EnvironmentVariable, Command


def generate_launch_description():
 
    #urdf_file_name = 'puzzlebot_hacker_ed.xacro'
    #urdf_file_name = 'puzzlebot_jetson_ed.xacro'
    urdf_file_name = 'puzzlebot_jetson_lidar_ed.xacro'
    urdf_default_path = os.path.join(
                        get_package_share_directory('puzzlebot_description'),
                        'urdf', 'mcr2_robots',
                        urdf_file_name)
   

    robot_state_pub_node = Node(
                            package='robot_state_publisher',
                            executable='robot_state_publisher',
                            name='robot_state_publisher',
                            output='screen',
                            parameters=[{'robot_description': ParameterValue(Command(['xacro ', str(urdf_default_path)]), value_type=str
                                )}],
                            )
    

    # Define joint_state_publisher node (for simulation)
    joint_state_publisher_node = Node(
                                package='joint_state_publisher_gui',
                                executable='joint_state_publisher_gui',
                                output='screen'
                            )   
    
    rviz_config = os.path.join(
                            get_package_share_directory('puzzlebot_description'),
                            'rviz',
                            'puzzlebot_desc.rviz'
                            )
    
    rviz_node = Node(name='rviz',
                    package='rviz2',
                    executable='rviz2',
                    arguments=['-d', rviz_config],
                    )
    
    


    
 

    l_d = LaunchDescription([
        robot_state_pub_node, 
        joint_state_publisher_node,
        rviz_node 
        ])

    return l_d