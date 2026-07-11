import rclpy
from rclpy.node import Node
from geometry_msgs.msg import Twist

class CircleTurtleNode(Node):
    def __init__(self):
        super().__init__('circle_turtle_node')
        # /turtle1/cmd_vel 토픽으로 Twist 타입의 메시지를 발행하는 퍼블리셔 생성 (큐 사이즈 10)
        self.publisher_ = self.create_publisher(Twist, '/turtle1/cmd_vel', 10)
        # 0.1초(10Hz)마다 타이머 콜백 함수 실행
        self.timer_ = self.create_timer(0.1, self.publish_velocity)
        self.get_logger().info('원형 주행 퍼블리셔 노드가 시작되었습니다.')

    def publish_velocity(self):
        msg = Twist()
        # 선속도 x축 방향으로 2.0 m/s (전진)
        msg.linear.x = 2.0
        msg.linear.y = 0.0
        msg.linear.z = 0.0
        # 각속도 z축 방향으로 1.0 rad/s (회전)
        msg.angular.x = 0.0
        msg.angular.y = 0.0
        msg.angular.z = 1.0
        
        # 메시지 발행
        self.publisher_.publish(msg)

def main(args=None):
    rclpy.init(args=args)
    node = CircleTurtleNode()
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        node.get_logger().info('노드가 종료되었습니다.')
    finally:
        node.destroy_node()
        rclpy.shutdown()

if __name__ == '__main__':
    main()