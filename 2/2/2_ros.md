# 과제 보고서: ROS2 개념 조사 및 실습 환경 구성

* **수행 목표:** ROS2 조사, ROS2 Humble 환경 구성 및 `ros2 run` 명령어 사용법 실습
* **개발 환경:** Ubuntu 22.04 LTS (Bash Shell), ROS2 Humble Hawksbill

---

## 1. 로봇 운영체제(ROS)의 개념 및 비교

### 1) 로봇 운영체제(ROS)의 개념
로봇 운영체제(ROS, Robot Operating System)는 일반적인 컴퓨터의 운영체제(Windows, Linux 등)와 달리 hardware 상에서 직접 실행되는 하드웨어 관리 OS가 아닙니다. 기존 운영체제 위에서 작동하며 로봇 개발에 필요한 다양한 도구, 라이브러리, 그리고 강력한 **도메인 간 통신 인프라(Middleware)**를 제공하는 **로봇 개발용 소프트웨어 플랫폼(메타 운영체제, Meta-OS)**입니다. 

로봇은 구동부, 센서, 제어 알고리즘 등 수많은 컴포넌트가 동시에 유기적으로 작동해야 하므로, ROS는 이들 간의 데이터 교환을 표준화된 방식으로 조율하는 핵심 역할을 합니다.

[Image of ROS2 Architecture and DDS Middleware]

### 2) 운영체제 사용 유무에 따른 로봇의 차이

| 구분 | OS를 사용하지 않는 로봇 (펌웨어/MCU 기반) | OS(ROS)를 사용하는 로봇 (고성능 프로세서/AP 기반) |
| :--- | :--- | :--- |
| **대표 제어기** | Arduino, STM32, AVR 등 (Bare-metal) | Raspberry Pi, Intel NUC, NVIDIA Jetson 등 |
| **제어 방식** | 하나의 거대한 메인 루프(`while(1)`) 내에서 센서 입력과 모터 제어가 순차적 혹은 인터럽트로 처리됨. | 기능별로 분리된 수