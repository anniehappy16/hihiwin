#open camara
https://github.com/realsenseai/realsense-ros.git

colcon build --symlink-install/n
source install/setup.bash
ros2 launch realsense2_camera rs_launch.py 
