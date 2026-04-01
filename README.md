# hihiwin 
/////初始化/////
1.下載主專案
git clone https://github.com/anniehappy16/hihiwin.git

cd src
2.下載相機套件
git clone https://github.com/realsenseai/realsense-ros.git
3.下載手臂套件
git clone https://github.com/tku-iarc/Hiwin_libmodbus

cd ..

/////執行ros2專案/////
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
