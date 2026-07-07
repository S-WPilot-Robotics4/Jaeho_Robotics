# 문제 6: ROS2 타이머와 콜백 학습

## 1. 타이머(Timer)와 콜백(Callback)의 개념
* **콜백(Callback):** 일반적인 프로그래밍에서 특정 이벤트(예: 버튼 클릭, 메시지 수신 등)가 발생했을 때 시스템에 의해 자동으로 호출되도록 등록해두는 함수를 의미합니다.
* **ROS2 타이머(Timer):** 로봇 제어 루프나 주기적인 센서 데이터 발행을 위해, 사용자가 지정한 시간 간격(예: 2초)마다 특정 콜백 함수를 반복해서 실행시켜 주는 기능입니다.

## 2. 코드 구현 및 실행 결과
`timer_test.py`에 2초 주기 타이머(counter 증가)와 3초 주기 타이머(counter 감소)를 구현하였으며, `rclpy.spin()`을 통해 프로그램이 종료되지 않고 주기적으로 콜백이 호출됨을 확인했습니다.

'''text
[INFO] [1783419162.679466816] [timer_node]: 2 seconds passed : 1
[INFO] [1783419163.673560299] [timer_node]: 3 seconds passed : 0
[INFO] [1783419164.673569140] [timer_node]: 2 seconds passed : 1
[INFO] [1783419166.673547364] [timer_node]: 2 seconds passed : 2
[INFO] [1783419166.673888282] [timer_node]: 3 seconds passed : 1
[INFO] [1783419168.673579153] [timer_node]: 2 seconds passed : 2
[INFO] [1783419169.673614093] [timer_node]: 3 seconds passed : 1
[INFO] [1783419170.673541153] [timer_node]: 2 seconds passed : 2
[INFO] [1783419172.673690810] [timer_node]: 2 seconds passed : 3
[INFO] [1783419172.674237148] [timer_node]: 3 seconds passed : 2
[INFO] [1783419174.673648818] [timer_node]: 2 seconds passed : 3
[INFO] [1783419175.673575333] [timer_node]: 3 seconds passed : 2
[INFO] [1783419176.673638731] [timer_node]: 2 seconds passed : 3
[INFO] [1783419178.673623322] [timer_node]: 2 seconds passed : 4
[INFO] [1783419178.673971741] [timer_node]: 3 seconds passed : 3
[INFO] [1783419180.673625085] [timer_node]: 2 seconds passed : 4
[INFO] [1783419181.673639673] [timer_node]: 3 seconds passed : 3
[INFO] [1783419182.673635374] [timer_node]: 2 seconds passed : 4
[INFO] [1783419184.673673283] [timer_node]: 2 seconds passed : 5
[INFO] [1783419184.674041152] [timer_node]: 3 seconds passed : 4
[INFO] [1783419186.673631347] [timer_node]: 2 seconds passed : 5
[INFO] [1783419187.673637061] [timer_node]: 3 seconds passed : 4
[INFO] [1783419188.673616886] [timer_node]: 2 seconds passed : 5
[INFO] [1783419190.673633608] [timer_node]: 2 seconds passed : 6
[INFO] [1783419190.674030032] [timer_node]: 3 seconds passed : 5
[INFO] [1783419192.673635152] [timer_node]: 2 seconds passed : 6
[INFO] [1783419193.673624207] [timer_node]: 3 seconds passed : 5
[INFO] [1783419194.673788339] [timer_node]: 2 seconds passed : 6
[INFO] [1783419196.673649376] [timer_node]: 2 seconds passed : 7
[INFO] [1783419196.674017973] [timer_node]: 3 seconds passed : 6
[INFO] [1783419198.673626203] [timer_node]: 2 seconds passed : 7
[INFO] [1783419199.673557703] [timer_node]: 3 seconds passed : 6
^C[INFO] [1783419200.487529598] [timer_node]: 프로그램이 종료되었습니다.

