import rclpy
from rclpy.node import Node
from geometry_msgs.msg import Twist
from turtlesim.msg import Pose
from turtlesim.srv import Spawn, Kill
from std_srvs.srv import Empty
import random
import math

class TurtleFollowNode(Node):
    def __init__(self):
        super().__init__('turtle_follow')
        
        # 1. 초기 상태 및 변수 선언
        self.current_robot = 1
        self.turtle_pose = None  # 위치 정보 (초기엔 데이터가 없으므로 None)
        self.next_location = [0.0, 0.0]
        
        # 2. Spawn 서비스 및 소환 실행
        self.spawn_client = self.create_client(Spawn, '/spawn')
        self.target_name = 'turtle2' # 추가 상태 변수
        self.state = 'INIT'          # 프로그램 진행 상태 플래그
        self.spawn_turtle()          # 노드 시작 시 거북이 소환 실행
        
        # 3. 퍼블리셔 및 서브스크라이버
        self.cmd_vel_publisher = self.create_publisher(Twist, '/turtle1/cmd_vel', 10)
        self.turtle_pose_subscriber = self.create_subscription(Pose, '/turtle1/pose', self.get_turtle_pose, 10)
        
        # 4. 기타 변수 및 남은 서비스/타이머 선언
        self.pose_msg = Pose()       # 정답 구조 맞춤용 
        self.kill_client = self.create_client(Kill, '/kill')
        self.quit_server = self.create_service(Empty, '/quit', self.quit_svr_callback)
        self.control_timer = self.create_timer(0.1, self.move_robot)


    def move_robot(self):
        # 추적 상태가 아니거나 내 위치를 모르면 대기
        if self.state != 'FOLLOWING' or self.turtle_pose is None:
            return

        dx = self.next_location[0] - self.turtle_pose.x
        dy = self.next_location[1] - self.turtle_pose.y
        distance = math.sqrt(dx**2 + dy**2)
        
        # 도달 기준을  0.1로  설정
        if distance < 0.1:
            self.get_logger().info('목표물 포획 성공! 추적자를 제거하고 프로그램을 종료합니다.')
            self.state = 'QUITTING'
            self.kill_turtle('turtle1', shutdown=True)
            return

        # P-Control 비례 제어 알고리즘 (지그재그가 아닌 부드럽고 자연스러운 궤적 유지)
        target_angle = math.atan2(dy, dx)
        angle_diff = target_angle - self.turtle_pose.theta
        
        # 각도를 -pi ~ pi 사이로 정규화
        angle_diff = math.atan2(math.sin(angle_diff), math.cos(angle_diff))

        msg = Twist()
        # 거리에 따른 선속도 비례 제어 (최소 속도 0.5 유지)
        msg.linear.x = max(1.5 * distance, 0.5) 
        msg.angular.z = 4.0 * angle_diff
        self.cmd_vel_publisher.publish(msg)

    def kill_turtle(self, name, shutdown=False):
        req = Kill.Request()
        req.name = name
        future = self.kill_client.call_async(req)
        # 셧다운 플래그가 True일 때만 노드 종료 콜백 연결
        if shutdown:
            future.add_done_callback(self.kill_turtle_response)

    def kill_turtle_response(self, future):
        # 노드 정상 종료
        raise SystemExit

    def get_turtle_pose(self, msg):
        self.turtle_pose = msg

    def spawn_turtle(self):
        while not self.spawn_client.wait_for_service(timeout_sec=1.0):
            self.get_logger().info('Spawn 서비스 대기 중...')
        
        req = Spawn.Request()
        corners = [
            (random.uniform(1.0, 2.5), random.uniform(1.0, 2.5)),    # 좌측 하단 구석
            (random.uniform(8.5, 10.0), random.uniform(1.0, 2.5)),  # 우측 하단 구석
            (random.uniform(1.0, 2.5), random.uniform(8.5, 10.0)),  # 좌측 상단 구석
            (random.uniform(8.5, 10.0), random.uniform(8.5, 10.0)) # 우측 상단 구석
        ]

        # 선택된 구석 구역의 x, y 좌표를 타겟 위치로 지정
        req.x, req.y = random.choice(corners)
        req.theta = random.uniform(-math.pi, math.pi) # 랜덤 방향 적용
        req.name = self.target_name
        
        self.next_location = [req.x, req.y]
        
        future = self.spawn_client.call_async(req)
        future.add_done_callback(self.spawn_turtle_response)

    def spawn_turtle_response(self, future):
        try:
            response = future.result()
            self.get_logger().info(f'목표물 소환 완료: {response.name} (x:{self.next_location[0]:.2f}, y:{self.next_location[1]:.2f})')
            self.state = 'FOLLOWING'
        except Exception as e:
            self.get_logger().error(f'소환 실패: {e}')

    def quit_svr_callback(self, request, response):
        self.get_logger().info('/quit 서비스 호출됨: 두 로봇을 모두 제거하고 종료합니다.')
        self.state = 'QUITTING'
        # 두 거북이를 제거, 마지막 호출에 shutdown 트리거 연동
        self.kill_turtle('turtle1', shutdown=False)
        self.kill_turtle(self.target_name, shutdown=True)
        return response

def main(args=None):
    rclpy.init(args=args)
    node = TurtleFollowNode()
    try:
        rclpy.spin(node)
    except (KeyboardInterrupt, SystemExit):
        # SystemExit를 받아 안전하게 종료 로깅
        node.get_logger().info('프로그램이 안전하게 정상 종료되었습니다.')
    finally:
        node.destroy_node()
        if rclpy.ok():
            rclpy.shutdown()

if __name__ == '__main__':
    main()