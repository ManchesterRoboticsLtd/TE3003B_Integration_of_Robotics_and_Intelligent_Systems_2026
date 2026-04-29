import os
from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument
from launch.substitutions import PathJoinSubstitution, LaunchConfiguration, TextSubstitution, Command, PythonExpression
from launch_ros.actions import Node
from launch_ros.parameter_descriptions import ParameterValue
from launch.conditions import IfCondition


def generate_launch_description():

    # Declare all possible launch arguments to make the launch file flexible
    declare_robot_name_arg = DeclareLaunchArgument('robot_name', default_value='Puzzlebot1', description='Name of the robot')
    declare_robot_arg = DeclareLaunchArgument('robot', default_value='puzzlebot_hacker_ed', description='Robot to be used')
    declare_x_arg = DeclareLaunchArgument('x', default_value='0.0', description='X position of the robot')
    declare_y_arg = DeclareLaunchArgument('y', default_value='0.0', description='Y position of the robot')
    declare_th_arg = DeclareLaunchArgument('yaw', default_value='0.0', description='Yaw angle of the robot')
    declare_sim_time_arg = DeclareLaunchArgument('use_sim_time', default_value='true', description='Use simulated time')
    declare_prefix_arg = DeclareLaunchArgument('prefix', default_value='', description='Prefix for robot links and namespaces')
    declare_camera_frame_arg = DeclareLaunchArgument('camera_frame', default_value='', description='Camera frame')
    declare_tof_frame_arg = DeclareLaunchArgument('tof_frame', default_value='', description='TOF sensor frame')
    declare_lidar_frame_arg = DeclareLaunchArgument('lidar_frame', default_value='', description='Lidar sensor frame')

    # Get launch configurations (parameters used later in launch file)
    robot_name = LaunchConfiguration('robot_name')
    robot = LaunchConfiguration('robot')
    x = LaunchConfiguration('x')
    y = LaunchConfiguration('y')
    yaw = LaunchConfiguration('yaw')
    use_sim_time = LaunchConfiguration('use_sim_time')
    prefix_name = LaunchConfiguration('prefix')
    camera_frame_name = LaunchConfiguration('camera_frame')
    tof_frame_name = LaunchConfiguration('tof_frame')
    lidar_frame_name = LaunchConfiguration('lidar_frame')

    # Get path to the package where robot models are stored
    models = get_package_share_directory('puzzlebot_description')

    # Generate robot_description dynamically by calling xacro with the selected parameters
    robot_description = Command([
        'xacro ',
        os.path.join(models, 'urdf', 'mcr2_robots') + '/',
        LaunchConfiguration('robot'),
        '.xacro ',
        'prefix:=', prefix_name, ' ',
        'lidar_frame:=', lidar_frame_name, ' ',
        'camera_frame:=', camera_frame_name, ' ',
        'tof_frame:=', tof_frame_name,
    ])

    # Node that publishes TF and joint states from robot_description
    robot_state_publisher_node = Node(
        package="robot_state_publisher",
        executable="robot_state_publisher",
        name="robot_state_publisher",
        output="screen",
        parameters=[{
            "robot_description": ParameterValue(robot_description, value_type=str),
            "use_sim_time": use_sim_time,
        }],
        namespace=prefix_name,
    )

    # Node that spawns the robot in Gazebo from its robot_description
    spawn_robot = Node(
        package="ros_gz_sim",
        executable="create",
        name='robot_spawner',
        arguments=[
            "-name", robot_name,
            "-topic", "robot_description",
            "-x", x, "-y", y, "-Y", yaw,
        ],
        namespace=prefix_name,
        output="screen",
    )

    # Bridge for puzzlebot_hacker_ed: publishes basic sensors and cmd_vel
    start_gazebo_ros_bridge_hacker_ed = Node(
        package='ros_gz_bridge',
        executable='parameter_bridge',
        name='robot_bridge',
        arguments=[
            [TextSubstitution(text='/'), prefix_name, TextSubstitution(text='ground_truth@nav_msgs/msg/Odometry[gz.msgs.Odometry')],
            [TextSubstitution(text='/'), prefix_name, TextSubstitution(text='VelocityEncL@std_msgs/msg/Float32[gz.msgs.Float')],
            [TextSubstitution(text='/'), prefix_name, TextSubstitution(text='VelocityEncR@std_msgs/msg/Float32[gz.msgs.Float')],
            [TextSubstitution(text='/'), prefix_name, TextSubstitution(text='joint_states@sensor_msgs/msg/JointState[gz.msgs.Model')],
            [TextSubstitution(text='/'), prefix_name, TextSubstitution(text='cmd_vel@geometry_msgs/msg/Twist]gz.msgs.Twist')],
        ],
        condition=IfCondition(PythonExpression(['"', robot, '" == "puzzlebot_hacker_ed"'])),
        namespace=prefix_name,
        output='screen'
    )

    # Bridge for puzzlebot_jetson_ed: includes camera and tof_scan
    start_gazebo_ros_bridge_jetson_ed = Node(
        package='ros_gz_bridge',
        executable='parameter_bridge',
        name='robot_bridge',
        arguments=[
            [TextSubstitution(text='/'), prefix_name, TextSubstitution(text='ground_truth@nav_msgs/msg/Odometry[gz.msgs.Odometry')],
            [TextSubstitution(text='/'), prefix_name, TextSubstitution(text='VelocityEncL@std_msgs/msg/Float32[gz.msgs.Float')],
            [TextSubstitution(text='/'), prefix_name, TextSubstitution(text='VelocityEncR@std_msgs/msg/Float32[gz.msgs.Float')],
            [TextSubstitution(text='/'), prefix_name, TextSubstitution(text='joint_states@sensor_msgs/msg/JointState[gz.msgs.Model')],
            [TextSubstitution(text='/'), prefix_name, TextSubstitution(text='camera_info@sensor_msgs/msg/CameraInfo[gz.msgs.CameraInfo')],
            [TextSubstitution(text='/'), prefix_name, TextSubstitution(text='tof_scan@sensor_msgs/msg/LaserScan[gz.msgs.LaserScan')],
            [TextSubstitution(text='/'), prefix_name, TextSubstitution(text='cmd_vel@geometry_msgs/msg/Twist]gz.msgs.Twist')],
        ],
        condition=IfCondition(PythonExpression(['"', robot, '" == "puzzlebot_jetson_ed"'])),
        namespace=prefix_name,
        output='screen'
    )

    # Bridge for puzzlebot_jetson_lidar_ed: adds LIDAR (scan) on top of the previous sensors
    start_gazebo_ros_bridge_jetson_lidar_ed = Node(
        package='ros_gz_bridge',
        executable='parameter_bridge',
        name='robot_bridge',
        arguments=[
            [TextSubstitution(text='/'), prefix_name, TextSubstitution(text='ground_truth@nav_msgs/msg/Odometry[gz.msgs.Odometry')],
            [TextSubstitution(text='/'), prefix_name, TextSubstitution(text='VelocityEncL@std_msgs/msg/Float32[gz.msgs.Float')],
            [TextSubstitution(text='/'), prefix_name, TextSubstitution(text='VelocityEncR@std_msgs/msg/Float32[gz.msgs.Float')],
            [TextSubstitution(text='/'), prefix_name, TextSubstitution(text='joint_states@sensor_msgs/msg/JointState[gz.msgs.Model')],
            [TextSubstitution(text='/'), prefix_name, TextSubstitution(text='camera_info@sensor_msgs/msg/CameraInfo[gz.msgs.CameraInfo')],
            [TextSubstitution(text='/'), prefix_name, TextSubstitution(text='tof_scan@sensor_msgs/msg/LaserScan[gz.msgs.LaserScan')],
            [TextSubstitution(text='/'), prefix_name, TextSubstitution(text='scan@sensor_msgs/msg/LaserScan[gz.msgs.LaserScan')],
            [TextSubstitution(text='/'), prefix_name, TextSubstitution(text='cmd_vel@geometry_msgs/msg/Twist]gz.msgs.Twist')],
        ],
        condition=IfCondition(PythonExpression(['"', robot, '" == "puzzlebot_jetson_lidar_ed"'])),
        namespace=prefix_name,
        output='screen'
    )

    # Image bridge that translates gz image -> ROS topics, remaps nested camera namespace to avoid double prefixes
    start_gazebo_ros_image_bridge_cmd = Node(
        package='ros_gz_image',
        executable='image_bridge',
        arguments=[
            PathJoinSubstitution([prefix_name, TextSubstitution(text='camera')])
        ],
        condition=IfCondition(PythonExpression(['"', robot, '" != "puzzlebot_hacker_ed"'])),
        namespace=prefix_name,
        remappings=[
            # Remap raw image
            (PathJoinSubstitution([TextSubstitution(text='/'), prefix_name, prefix_name, 'camera']),
             PathJoinSubstitution([TextSubstitution(text='/'), prefix_name, 'camera'])),

            # Remap compressed image topics
            (PathJoinSubstitution([TextSubstitution(text='/'), prefix_name, prefix_name, 'camera', 'compressed']),
             PathJoinSubstitution([TextSubstitution(text='/'), prefix_name, 'camera', 'compressed'])),

            (PathJoinSubstitution([TextSubstitution(text='/'), prefix_name, prefix_name, 'camera', 'compressedDepth']),
             PathJoinSubstitution([TextSubstitution(text='/'), prefix_name, 'camera', 'compressedDepth'])),

            (PathJoinSubstitution([TextSubstitution(text='/'), prefix_name, prefix_name, 'camera', 'theora']),
             PathJoinSubstitution([TextSubstitution(text='/'), prefix_name, 'camera', 'theora'])),
        ],
        output='screen'
    )

    # Final launch description list of all declared arguments and nodes
    l_d = [
        declare_robot_name_arg, declare_robot_arg, declare_x_arg, declare_y_arg, declare_th_arg, declare_sim_time_arg, declare_prefix_arg,
        robot_state_publisher_node, spawn_robot,
        start_gazebo_ros_bridge_hacker_ed, start_gazebo_ros_bridge_jetson_lidar_ed, start_gazebo_ros_bridge_jetson_ed,
        start_gazebo_ros_image_bridge_cmd,
        declare_camera_frame_arg, declare_tof_frame_arg, declare_lidar_frame_arg
    ]

    return LaunchDescription(l_d)