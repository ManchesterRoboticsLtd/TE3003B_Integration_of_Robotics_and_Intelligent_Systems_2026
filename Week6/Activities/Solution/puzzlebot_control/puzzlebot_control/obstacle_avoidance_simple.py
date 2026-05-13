import rclpy
from rclpy.node import Node
from geometry_msgs.msg import Twist
from sensor_msgs.msg import LaserScan
import numpy as np
import signal

class ObstacleAvoidance(Node):
    def __init__(self):
        super().__init__('obstacle_avoidance_node')

        self.wait_for_ros_time()

        self.publisher_ = self.create_publisher(Twist, 'robot1/cmd_vel', 10)
        self.subscription = self.create_subscription(
            LaserScan, 'robot1/scan', self.scan_callback, 10)

        self.obstacle_threshold = 0.5  # Obstacle detection distance threshold (meters)
        self.forward_angle_width = 30  # Degrees to check directly ahead (±15 degrees)

        self.get_logger().info("Obstacle Avoidance Node Started.")

    def scan_callback(self, msg: LaserScan):
        ranges = np.array(msg.ranges)

        # Convert forward angle width to radians and calculate half-angle
        half_angle = np.radians(self.forward_angle_width / 2)

        # Center index for the scan array (angle 0 rad is directly forward)
        idx_center = 0

        # Angle between each LiDAR measurement
        angle_increment = msg.angle_increment

        # Total number of points in one full 360-degree LiDAR scan
        num_points = len(ranges)

        # Determine how many indices correspond to half the angle width ahead
        idx_offset = int(half_angle / angle_increment)

        # Generate a list of indices around the front of the robot
        # E.g., [-15, -14, ..., -1, 0, 1, ..., 14, 15] for ±15 degrees
        indices = list(range(-idx_offset, idx_offset + 1))

        # Wrap-around indices using modulo to handle negative indices properly
        front_indices = [(idx_center + idx) % num_points for idx in indices]

        # Select the distance measurements directly in front of the robot
        front_ranges = ranges[front_indices]

        # Check if any obstacles are within the threshold distance in front
        if np.any(front_ranges < self.obstacle_threshold):
            self.get_logger().info('Obstacle detected! Turning...')
            self.turn()
        else:
            self.move_forward()

    def move_forward(self):
        twist = Twist()
        twist.linear.x = 0.2
        twist.angular.z = 0.3
        self.publisher_.publish(twist)

    def turn(self):
        twist = Twist()
        twist.linear.x = 0.0
        twist.angular.z = 0.5
        self.publisher_.publish(twist)

    def wait_for_ros_time(self):
        self.get_logger().info('Waiting for ROS time to become active...')
        while rclpy.ok():
            now = self.get_clock().now()
            if now.nanoseconds > 0:
                break
            rclpy.spin_once(self, timeout_sec=0.1)
        self.get_logger().info(f'ROS time is active! Start time: {now.nanoseconds * 1e-9:.2f}s')

    def stop_handler(self,signum, frame):
        """Handles Ctrl+C (SIGINT)."""
        self.get_logger().info("Interrupt received! Stopping node...")
        raise SystemExit

def main(args=None):

    rclpy.init(args=args)

    node = ObstacleAvoidance()

    signal.signal(signal.SIGINT, node.stop_handler)

    try:
        rclpy.spin(node)
    except SystemExit:
        node.get_logger().info('SystemExit triggered. Shutting down cleanly.')
    finally:
        # Make sure the robot stops completely upon shutdown
        twist = Twist()
        twist.linear.x = 0.0
        twist.angular.z = 0.0
        node.publisher_.publish(twist)

        node.destroy_node()
        rclpy.shutdown()

if __name__ == '__main__':
    main()
