import rclpy
from rclpy.node import Node
from geometry_msgs.msg import Twist
from nav_msgs.msg import Odometry
from std_msgs.msg import Float32
import numpy as np
import transforms3d

class KinematicModelNode(Node):
    def __init__(self):
        super().__init__('kinematic_model')

        #Set the parameters of the system
        self.x = 0.0
        self.y = 0.0
        self.theta = 0.0
        self._l = 0.19
        self._r = 0.05
        self._k_r = 0.016
        self._k_l = 0.016
        self._sample_time = 0.01

        # Velocity inputs
        self.v = 0.0  # Linear velocity (m/s)
        self.omega = 0.0  # Angular velocity (rad/s)

        #Messages to be used
        self.wr = Float32()
        self.wl = Float32()

        # Last update time
        self.last_time = self.get_clock().now()

        # ROS2 Subscribers and Publishers
        self.create_subscription(Twist, 'cmd_vel', self.cmd_vel_callback, 10)
        self.wl_pub = self.create_publisher(Float32, 'wl', 10)
        self.wr_pub = self.create_publisher(Float32, 'wr', 10)

        # Timer to update kinematics at ~100Hz
        self.timer = self.create_timer(self._sample_time, self.update_kinematics)  # 100 Hz

        self.get_logger().info("Kinematic Model Node Started.")

    def cmd_vel_callback(self, msg):
        """ Callback to update velocity commands """
        self.v = msg.linear.x
        self.omega = msg.angular.z

    def update_kinematics(self):
        """ Updates robot position based on real elapsed time """
        # Get current time and compute dt
        current_time = self.get_clock().now()
        dt = (current_time - self.last_time).nanoseconds / 1e9  # Convert to seconds
        self.last_time = current_time

        if dt > 0:
            # Simulate the encoders data
            omega_r = (self.v + self._l * self.omega / 2.0) / self._r 
            omega_l = (self.v - self._l * self.omega / 2.0) / self._r

            #Simulate encoders with added noise
            self.wr.data = omega_r + np.random.normal(0,self._k_r * np.abs(omega_r))
            self.wl.data = omega_l  + np.random.normal(0,self._k_l * np.abs(omega_l))

            # Publish new state
            self.publish_wheel_speed()

    def publish_wheel_speed(self):
        self.wl_pub.publish(self.wl)
        self.wr_pub.publish(self.wr)

def main(args=None):

    rclpy.init(args=args)

    node = KinematicModelNode()

    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    finally:
        if rclpy.ok():  # Ensure shutdown is only called once
            rclpy.shutdown()
        node.destroy_node()

if __name__ == '__main__':
    main()