import rclpy
from rclpy.node import Node
from turtlesim.msg import Pose

class TurtlePoseSubscriber(Node):
    def __init__(self):
        super().__init__('turtle_pose_subscriber')
        # /turtle1/pose 토픽을 구독하는 서브스크라이버 생성
        self.subscription = self.create_subscription(
            Pose,
            '/turtle1/pose',
            self.pose_callback,
            10)
        self.subscription  # 사용되지 않는 변수 경고 방지
        
        # 이전 상태(x, y, theta)를 저장할 변수 초기화
        self.prev_x = None
        self.prev_y = None
        self.prev_theta = None
        
        self.get_logger().info('거북이 위치 추적 서브스크라이버가 시작되었습니다.')

    def pose_callback(self, msg):
        # 메시지에서 속도를 제외한 위치/방향 값만 추출 (소수점 4자리까지 반올림)
        current_x = round(msg.x, 4)
        current_y = round(msg.y, 4)
        current_theta = round(msg.theta, 4)

        # 이전 상태와 비교하여 하나라도 값이 바뀌었을 때만 로그 출력
        if (self.prev_x != current_x) or (self.prev_y != current_y) or (self.prev_theta != current_theta):
            self.get_logger().info(f'위치 갱신 -> X: {current_x}, Y: {current_y}, Theta: {current_theta}')
            
            # 현재 상태를 이전 상태로 업데이트
            self.prev_x = current_x
            self.prev_y = current_y
            self.prev_theta = current_theta

def main(args=None):
    rclpy.init(args=args)
    node = TurtlePoseSubscriber()
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        node.get_logger().info('서브스크라이버 노드가 종료되었습니다.')
    finally:
        node.destroy_node()
        rclpy.shutdown()

if __name__ == '__main__':
    main()