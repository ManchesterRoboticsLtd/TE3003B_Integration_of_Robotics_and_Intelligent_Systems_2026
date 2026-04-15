import rclpy
from rclpy.node import Node
from nav_msgs.msg import Odometry
from std_msgs.msg import Float32
import numpy as np
import transforms3d
import signal

class DeadReckoning(Node):
    def __init__(self):
        super().__init__('localisation_node')

    #WRITE YOUR CODE HERE

def main(args=None):

    rclpy.init(args=args)

    node = DeadReckoning()

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