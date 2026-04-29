import os
from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch.actions import (
    DeclareLaunchArgument, SetEnvironmentVariable, IncludeLaunchDescription
)
from launch.substitutions import PathJoinSubstitution, LaunchConfiguration, TextSubstitution
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch.conditions import IfCondition, UnlessCondition
from launch_ros.actions import Node


def generate_launch_description():
    # ----------------------
    # Declare Launch Arguments
    # ----------------------
    declare_world_arg = DeclareLaunchArgument(
        'world',
        default_value='puzzlebot_arena.world',
        description='Gazebo world file to load'
    )

    declare_pause_arg = DeclareLaunchArgument(
        'pause',
        default_value='false',
        description='Start Gazebo paused'
    )

    declare_verbosity_arg = DeclareLaunchArgument(
        'verbosity',
        default_value='4',
        description='Gazebo verbosity level (0-4)'
    )

    # ----------------------
    # Launch Configurations
    # ----------------------
    pause = LaunchConfiguration('pause')
    world_file = LaunchConfiguration('world')
    gazebo_verbosity = LaunchConfiguration('verbosity')

    # ----------------------
    # Get Package Directories
    # ----------------------
    pkg_ros_gz_sim = get_package_share_directory('ros_gz_sim')
    gazebo_resources = get_package_share_directory('puzzlebot_gazebo')

    # ----------------------
    # Gazebo Resource Paths
    # ----------------------
    world_path = PathJoinSubstitution([gazebo_resources,'worlds', world_file])
    gazebo_models_path = os.path.join(gazebo_resources, 'models')
    gazebo_plugins_path = os.path.join(gazebo_resources, 'plugins')
    gazebo_media_path = os.path.join(gazebo_models_path, 'models', 'media', 'materials')

    # ----------------------
    # Set Gazebo Environment Variables
    # ----------------------
    set_gazebo_resources = SetEnvironmentVariable(
        name='GZ_SIM_RESOURCE_PATH',
        value=f"{gazebo_models_path}:{gazebo_media_path}"
    )

    set_gazebo_plugins = SetEnvironmentVariable(
        name='GZ_SIM_SYSTEM_PLUGIN_PATH',
        value=f"{gazebo_plugins_path}"
    )

    # ----------------------
    # Include Gazebo Launch File
    # ----------------------
    gz_launch_path = PathJoinSubstitution([pkg_ros_gz_sim, 'launch', 'gz_sim.launch.py'])

    start_gazebo_server_run = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(gz_launch_path),
        launch_arguments={
        'gz_args': ['-r ','-v ', gazebo_verbosity, ' ', world_path],
        'on_exit_shutdown': 'true',
        }.items(),
        condition=UnlessCondition(pause)
    )

    start_gazebo_server_paused = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(gz_launch_path),
        launch_arguments={
            'gz_args':  ['-v ', gazebo_verbosity, ' ', world_path],
            'on_exit_shutdown': 'true',
            'pause': 'true',
        }.items(),
        condition=IfCondition(pause)
    )

    start_gazebo_ros_bridge_cmd = Node(
                    package='ros_gz_bridge',
                    executable='parameter_bridge',
                    name='time_bridge',
                    arguments=[
                   '/clock@rosgraph_msgs/msg/Clock[gz.msgs.Clock',
                   '/tf@tf2_msgs/msg/TFMessage[gz.msgs.Pose_V',
                   ],
                    output='screen'
                    )

    # ----------------------
    # Launch Description List
    # ----------------------
    return LaunchDescription([
        declare_world_arg,
        declare_pause_arg,
        declare_verbosity_arg,
        set_gazebo_resources,
        set_gazebo_plugins,
        start_gazebo_server_run,
        start_gazebo_server_paused,
        start_gazebo_ros_bridge_cmd
    ])