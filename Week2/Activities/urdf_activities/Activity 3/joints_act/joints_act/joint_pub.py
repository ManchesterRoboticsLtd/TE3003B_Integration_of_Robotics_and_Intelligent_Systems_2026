
import rclpy
from rclpy.node import Node
from sensor_msgs.msg import JointState
import numpy as np

class FramePublisher(Node):

    def __init__(self):
        super().__init__('joints_publisher')
	
	#WRITE YOUR CODE HERE
	
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
