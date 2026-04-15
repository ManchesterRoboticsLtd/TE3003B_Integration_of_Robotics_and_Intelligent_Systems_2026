# Imports
import rclpy
from rclpy.node import Node
from std_msgs.msg import Float32

#Class Definition
class DCMotor(Node):
    def __init__(self):
        super().__init__('dc_motor')
        

#Main
def main(args=None):
    rclpy.init(args=args)

    node = DCMotor()

    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    finally:
        node.destroy_node()
        rclpy.try_shutdown()

#Execute Node
if __name__ == '__main__':
    main()
