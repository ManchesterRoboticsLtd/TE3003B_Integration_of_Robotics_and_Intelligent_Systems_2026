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


    # Robot 1: group1

    robot1_state_pub = Node(
        package='robot_state_publisher',
        executable='robot_state_publisher',
        name='robot_state_publisher',
        output='screen',
        parameters=[{'frame_prefix': 'group1/','robot_description': robot_desc}],
        namespace='group1'
    )

    joint_state_publisher_node = Node(
                                package='joint_state_publisher_gui',
                                executable='joint_state_publisher_gui',
                                output='screen',
                                namespace='group1'
                            )

    robot1_node = Node(
        name='puzzledrone',
        package='puzzle_drone',
        executable='puzzledrone_joint_state_pub',
        namespace='group1',
        parameters=[{
                    'init_pose_x':2.0,
                    'init_pose_y': 2.0,
                    'init_pose_z': 1.0,
                    'init_pose_yaw': 1.57,
                    'init_pose_pitch': 0.0,
                    'init_pose_roll': 0.0,
                    'odom_frame':'odom'
                }]
            )   


    # Robot 2: group2
    
    robot2_state_pub = Node(
        package='robot_state_publisher',
        executable='robot_state_publisher',
        name='robot_state_publisher',
        output='screen',
        parameters=[{'frame_prefix': 'group2/','robot_description': robot_desc}],
        namespace='group2'
    )

    joint_state_publisher_node2 = Node(
                                package='joint_state_publisher_gui',
                                executable='joint_state_publisher_gui',
                                output='screen',
                                namespace='group2'
                            )

    robot2_node = Node(
        name='puzzledrone',
        package='puzzle_drone',
        executable='puzzledrone_joint_state_pub',
        namespace='group2',
        parameters=[{
                    'init_pose_x':-2.0,
                    'init_pose_y': 2.0,
                    'init_pose_z': 1.0,
                    'init_pose_yaw': 1.57,
                    'init_pose_pitch': 0.0,
                    'init_pose_roll': 0.0,
                    'odom_frame':'odom'
                }]
            )   
    
    rviz_config = os.path.join(
                            get_package_share_directory('puzzle_drone'),
                            'rviz',
                            'multi_puzzle_drone.rviz'
                            )
    
    rviz_node = Node(name='rviz',
                    package='rviz2',
                    executable='rviz2',
                    arguments=['-d', rviz_config],
                    )

    
    return LaunchDescription([
        robot1_state_pub,
        robot1_node,
        robot2_state_pub,
        robot2_node,
        rviz_config,
        rviz_node
    ])