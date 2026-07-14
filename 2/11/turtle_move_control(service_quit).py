import rclpy
from rclpy.node import Node
from geometry_msgs.msg import Twist
from turtlesim.msg import Pose
from turtlesim.srv import Kill
from std_srvs.srv import Empty

class TurtleMoveControlNode(Node):
    def __init__(self):
        super().__init__('turtle_move_control')
        
        # 1. 퍼블리셔: 속도 제어 명령 내리기
        self.publisher_ = self.create_publisher(Twist, '/turtle1/cmd_vel', 10)
        
        # 2. 서브스크라이버: 현재 위치 받아오기
        self.subscription = self.create_subscription(Pose, '/turtle1/pose', self.pose_callback, 10)
        
        # 3. 타이머: 0.1초마다 제어 로직 실행
        self.timer = self.create_timer(0.1, self.timer_callback)

        # 4. 클라이언트: 거북이를 지우는 /kill 서비스 요청용
        self.kill_client = self.create_client(Kill, '/kill')

        # 5. 서버: 외부에서 이 노드를 끄기 위해 호출할 /quit 서비스 제공용
        self.quit_server = self.create_service(Empty, '/quit', self.quit_callback)
        
        self.current_pose = None
        self.turn_mode = False  # 회전 모드 상태 플래그
        self.is_quitting = False # 종료 프로세스가 시작되었는지 확인하는 플래그
        
        self.get_logger().info('벽 회피 자율주행 제어 노드가 시작되었습니다. 종료하려면 /quit 서비스를 호출하세요.')

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
        # 위치를 못 받았거나, 종료 중 (/quit 호출됨)일 때는 로봇을 멈춤
        if self.current_pose is None or self.is_quitting:
            return
            
        msg = Twist()
        
        if self.turn_mode:
            # 벽에 가까우면 곡선을 그리며 회전 (선속도 조금, 각속도 많이)
            msg.linear.x = 1.0
            msg.angular.z = 2.5 
            
        else:
            # 안전 구역이면 시원하게 직진
            msg.linear.x = 3.0
            msg.angular.z = 0.0
            
        self.publisher_.publish(msg)


    def quit_callback(self, request, response):
        # /quit 서비스가 호출되었을 때 실행되는 콜백 함수
        self.get_logger().info('/quit 서비스 호출됨: 거북이를 제거하고 노드를 종료합니다...')
        self.is_quitting = True # 주행 타이머 중지

        # 거북이를 지우는 /kill 서비스 비동기 (Async) 호출
        # (결과를 기다리는 동안 프로그램이 멈추지 않고 하던 일을 계속할 수 있게 함)
        req = Kill.Request()
        req.name = 'turtle1'
        future = self.kill_client.call_async(req)

        # /kill 서비스가 완료되면 실행할 마무리 함수 연결
        future.add_done_callback(self.kill_done_callback)

        return response

    def kill_done_callback(self, future):
        # /kill 호출이 완료된 직후 실행되는 함수
        try:
            future.result()
            self.get_logger().info('거북이(turtle1)가 시뮬레이터에서 성공적으로 지워졌습니다.')
        except Exception as e:
            self.get_logger().error(f' 서비스 호출 실패: {e}')

        # 우아한 종료: 처리되지 않은 예외(빨간 에러) 없이 메인 스레드의 spin()을 정상 종료시킴
        raise SystemExit

def main(args=None):
    rclpy.init(args=args)
    node = TurtleMoveControlNode()
    try:
        rclpy.spin(node)
    except (KeyboardInterrupt,SystemExit): # SystemExit를 잡아서 정상 종료 처리
        node.get_logger().info('제어 노드가 안전하게 정상 종료되었습니다.')
    finally:
        node.destroy_node()
        # 이미 종료되지 않은 경우에만 shutdown 호출
        if rclpy.ok():
            rclpy.shutdown()

if __name__ == '__main__':
    main()