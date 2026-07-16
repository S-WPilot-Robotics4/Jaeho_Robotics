import os
from launch import LaunchDescription
from launch_ros.actions import Node

def generate_launch_description():
    return LaunchDescription([
        # 1. 거북이 시뮬레이터 노드 실행
        Node(
            package='turtlesim',
            executable='turtlesim_node',
            name='turtlesim',
            output='screen'
        ),
        # 2. 우리가 만든 자율주행 제어 노드 실행
        Node(
            package='my_robot_controller',
            executable='turtle_move_control',
            name='turtle_move_control',
            output='screen'
        )
    ])