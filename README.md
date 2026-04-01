# hihiwin
git clone https://github.com/anniehappy16/hihiwin.git

#git clone
cd src
1.realsenseai
git clone https://github.com/realsenseai/realsense-ros.git
2.Hiwin_libmodbus
git clone https://github.com/tku-iarc/Hiwin_libmodbus

cd ..


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


#git note
1.git add .
2.git commit -m "xxx"
3.git push
