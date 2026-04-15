import rclpy
from rclpy.node import Node
from geometry_msgs.msg import Twist
from nav_msgs.msg import Odometry
from std_msgs.msg import Float32
import numpy as np
import transforms3d

class PointStabilisationNode(Node):
    def __init__(self):

        #WRITE YOUR CODE HERE

def main(args=None):

    rclpy.init(args=args)

    node = PointStabilisationNode()

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