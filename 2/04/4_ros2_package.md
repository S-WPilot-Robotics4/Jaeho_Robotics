# ROS2 패키지 및 파이썬 빌드 시스템 조사

## 1. ROS2 colcon 명령어
`colcon`은 ROS2에서 워크스페이스 내의 패키지들을 빌드하고 테스트하기 위해 사용하는 범용 빌드 시스템(도구)입니다. 기존 ROS1의 `catkin_make`를 대체하며, 워크스페이스 루트 디렉토리(`~/ros2_ws`)에서 `colcon build` 명령을 실행하면 `src` 폴더에 있는 소스코드들을 컴파일하고, 실행 가능한 형태로 구성하여 `build`, `install`, `log` 디렉토리를 자동으로 생성합니다. `colcon` 명령어를 찾을 수 없다는 오류가 발생할 경우, 터미널에 `source /opt/ros/humble/setup.bash` 환경설정 스크립트를 실행하지 않았기 때문입니다.

## 2. 파이썬 빌드 시스템 (`ament_python`)과 rclpy
* **ament_python:** ROS2에서 Python으로 작성된 노드와 패키지를 빌드하기 위한 빌드 시스템입니다. 내부적으로 표준 파이썬 패키징 도구인 `setuptools`를 활용하며, `setup.py` 파일을 통해 패키지를 설치하고 관리합니다.
* **rclpy (ROS Client Library for Python):** 개발자가 Python을 사용해 ROS2 노드(Node)를 작성할 수 있도록 돕는 ROS2의 공식 파이썬 API 라이브러리입니다. 토픽 발행/구독(Publish/Subscribe), 서비스, 액션 등 ROS2의 핵심 통신 기능들을 파이썬 코드로 쉽게 구현할 수 있게 해줍니다.

## 3. ros2 pkg create 명령어 사용법
ROS2에서 새로운 패키지를 생성할 때 사용하는 명령어입니다. 
* **기본 문법:** `ros2 pkg create <패키지이름> --build-type <빌드타입> --dependencies <의존성1> <의존성2>`
* 본 실습에서는 `ros2 pkg create my_robot_controller --build-type ament_python --dependencies rclpy` 명령을 사용하여 파이썬 기반의 패키지를 생성하고 `rclpy` 라이브러리를 의존성으로 추가했습니다.

## 4. package.xml 과 setup.py 파일의 역할
ROS2 파이썬 패키지를 구성하는 가장 핵심적인 두 파일입니다.
* **`package.xml`:** 패키지의 메타데이터를 담고 있는 XML 파일입니다. 패키지의 이름, 버전, 작성자, 라이선스 정보뿐만 아니라, 이 패키지가 실행되거나 빌드될 때 어떤 다른 패키지(예: `rclpy`)가 필요한지 의존성 관계를 명시합니다.
* **`setup.py`:** 파이썬 패키지의 설치 설정 파일입니다. 노드가 실행될 때 어떤 파이썬 스크립트 파일을 실행해야 하는지 `entry_points` 항목에 정의하며, `ros2 run` 명령어를 쳤을 때 실제 구동될 실행 파일명과 함수를 연결해 주는 역할을 합니다.

## 5. 워크스페이스 트리(tree) 실행 결과
패키지 생성 후 `~/ros2_ws` 디렉토리에서 `tree` 명령어를 실행한 결과, `build`, `install`, `log` 폴더와 함께 `src` 디렉토리 내부에 `my_robot_controller` 패키지가 정상적으로 구성된 것을 확인했습니다.

```text
.
├── build
├── install
├── log
└── src
    └── my_robot_controller
        ├── my_robot_controller
        │   └── __init__.py
        ├── package.xml
        ├── resource
        │   └── my_robot_controller
        ├── setup.cfg
        ├── setup.py
        └── test
            ├── test_copyright.py
            ├── test_flake8.py
            └── test_pep257.py