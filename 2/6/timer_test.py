import rclpy
from rclpy.node import Node

class TimerNode(Node):
    def __init__(self):
        super().__init__('timer_node')
        # 1. 클래스 속성으로 counter 변수 초기화
        self.counter = 0
        
        # 2. 타이머 생성 (주기 단위: 초, 콜백 함수 지정)
        self.timer_2s = self.create_timer(2.0, self.timer_2s_callback)
        self.timer_3s = self.create_timer(3.0, self.timer_3s_callback)

    # 2초마다 실행되는 콜백 함수
    def timer_2s_callback(self):
        self.counter += 1
        self.get_logger().info(f'2 seconds passed : {self.counter}')

    # 3초마다 실행되는 콜백 함수
    def timer_3s_callback(self):
        self.counter -= 1
        self.get_logger().info(f'3 seconds passed : {self.counter}')

def main(args=None):
    rclpy.init(args=args)
    node = TimerNode()
    
    try:
        # 노드가 종료될 때까지 콜백 함수들을 계속 대기시키고 실행함
        rclpy.spin(node)
    except KeyboardInterrupt:
        node.get_logger().info('프로그램이 종료되었습니다.')
    finally:
        node.destroy_node()
        rclpy.shutdown()

if __name__ == '__main__':
    main()