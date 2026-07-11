import rclpy
from rclpy.node import Node

# Node 클래스를 상속받아 사용자 정의 노드 생성
class LoggingNode(Node):
    def __init__(self):
        # 부모 클래스의 생성자를 호출하며 노드의 이름을 'logging_node'로 지정
        super().__init__('logging_node')
        # INFO 수준의 로그로 노드 이름 출력
        self.get_logger().info('logging_node')

def main(args=None):
    # ROS2 통신 초기화
    rclpy.init(args=args)
    
    # 노드 객체 생성
    node = LoggingNode()
    
    # 프로그램이 종료되지 않고 계속 실행 상태를 유지하도록 설정
    rclpy.spin(node)
    
    # 노드 파괴 및 ROS2 통신 종료 (Ctrl+C 입력 시 실행됨)
    node.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()