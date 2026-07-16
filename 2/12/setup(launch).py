import os
from glob import glob
from setuptools import find_packages, setup

package_name = 'my_robot_controller'

setup(
    name=package_name,
    version='0.0.0',
    packages=find_packages(exclude=['test']),
    data_files=[
        ('share/ament_index/resource_index/packages',
            ['resource/' + package_name]),
        ('share/' + package_name, ['package.xml']),
        (os.path.join('share', package_name, 'launch'), glob('launch/*.launch.py')),
    ],
    install_requires=['setuptools'],
    zip_safe=True,
    maintainer='hohojae',
    maintainer_email='joleam024@gmail.com',
    description='TODO: Package description',
    license='TODO: License declaration',
    tests_require=['pytest'],
    entry_points={
        'console_scripts': [
                'logging_node = my_robot_controller.logging:main',
                'timer_test = my_robot_controller.timer_test:main',
                'circle_turtle = my_robot_controller.circle_turtle:main',
                'turtle_pose = my_robot_controller.turtle_pose:main',
                'turtle_move_control = my_robot_controller.turtle_move_control:main',
        ],
    },
)
