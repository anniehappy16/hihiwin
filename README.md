# hihiwin
#open realsense

colcon build --symlink-install
source install/setup.bash
ros2 launch realsense2_camera rs_align_depth_launch.py 

#yolo node 
colcon build
source install/setup.bash
ros2 run yolo yolo_sub

#connect hiwin
colcon build
source install/setup.bash
ros2 run hiwin_libmodbus hiwinlibmodbus_server

#run hiwin
colcon build
source install/setup.bash
ros2 run hiwin_example strategy_example 
