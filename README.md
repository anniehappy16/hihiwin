#open camara
https://github.com/realsenseai/realsense-ros.git

##opren realsense ROS2
colcon build --symlink-install
source install/setup.bash
ros2 launch realsense2_camera rs_launch.py 
