
import rclpy
from rclpy.node import Node
from sensor_msgs.msg import JointState
import numpy as np

class FramePublisher(Node):

    def __init__(self):
        super().__init__('joints_publisher')

        #Publisher
        self.publisher = self.create_publisher(JointState, '/joint_states', 10)
        
        #Create a Timer
        timer_period = 0.1 #seconds
        self.timer = self.create_timer(timer_period, self.timer_cb)

        #initialise Message to be published
        self.ctrlJoints = JointState()
        self.ctrlJoints.header.stamp = self.get_clock().now().to_msg()
        self.ctrlJoints.name = ["joint_revolute", "joint_prismatic", "joint_continuous_1", "joint_continuous_2"]
        self.ctrlJoints.position = [0.0] * 4
        self.ctrlJoints.velocity = [0.0] * 4
        self.ctrlJoints.effort = [0.0] * 4

        #Initialise Variables
        self.i = 0.0
        self.sign = 1

    #Timer Callback
    def timer_cb(self):

        time = self.get_clock().now().nanoseconds/1e9

        self.ctrlJoints.header.stamp = self.get_clock().now().to_msg()
        self.ctrlJoints.position[0] = -0.785 + 2*0.785*self.i
        self.ctrlJoints.position[1] = -2+4.0*self.i
        self.ctrlJoints.position[2] = 0.5*time
        self.ctrlJoints.position[3] = 0.5*time
        
        if self.i > 1:
            self.sign = -1
        elif self.i  < 0:
            self.sign = 1
        self.i  = self.i  + self.sign*0.1

        self.publisher.publish(self.ctrlJoints)

def main(args=None):
    rclpy.init(args=args)
    node = FramePublisher()
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