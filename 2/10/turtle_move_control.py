import rclpy
from rclpy.node import Node
from geometry_msgs.msg import Twist
from turtlesim.msg import Pose

class TurtleMoveControlNode(Node):
    def __init__(self):
        super().__init__('turtle_move_control')
        
        # 1. 퍼블리셔: 속도 제어 명령 내리기
        self.publisher_ = self.create_publisher(Twist, '/turtle1/cmd_vel', 10)
        
        # 2. 서브스크라이버: 현재 위치 받아오기
        self.subscription = self.create_subscription(Pose, '/turtle1/pose', self.pose_callback, 10)
        
        # 3. 타이머: 0.1초마다 제어 로직 실행
        self.timer = self.create_timer(0.1, self.timer_callback)
        
        self.current_pose = None
        self.turn_mode = False  # 회전 모드 상태 플래그
        
        self.get_logger().info('벽 회피 자율주행 제어 노드가 시작되었습니다.')

    def pose_callback(self, msg):
        self.current_pose = msg
        
        # turtlesim 맵 크기는 대략 0.0 ~ 11.08 입니다.
        # 벽에서 2.0 거리 이내로 가까워지면 회전 모드로 전환합니다.
        margin = 2.0
        if (msg.x < margin or msg.x > 11.08 - margin or
            msg.y < margin or msg.y > 11.08 - margin):
            self.turn_mode = True
        else:
            self.turn_mode = False

    def timer_callback(self):
        # 아직 위치 데이터를 한 번도 못 받았다면 대기
        if self.current_pose is None:
            return
            
        msg = Twist()
        
        if self.turn_mode:
            # 벽에 가까우면 곡선을 그리며 회전 (선속도 조금, 각속도 많이)
            msg.linear.x = 1.0
            msg.angular.z = 2.5 
            self.get_logger().info('벽 감지! 곡선 회전 중...')
        else:
            # 안전 구역이면 시원하게 직진
            msg.linear.x = 3.0
            msg.angular.z = 0.0
            
        self.publisher_.publish(msg)

def main(args=None):
    rclpy.init(args=args)
    node = TurtleMoveControlNode()
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        node.get_logger().info('제어 노드가 종료되었습니다.')
    finally:
        node.destroy_node()
        rclpy.shutdown()

if __name__ == '__main__':
    main()