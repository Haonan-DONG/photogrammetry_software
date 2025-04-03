# Usage
## add gps info for the video, recorded by DJI
g++ -o add_gps add_gps.cpp -lexiv2 -lboost_system -lboost_filesystem -I /usr/include/eigen3/ -lopencv_core -lopencv_imgcodecs -lopencv_highgui -lopencv_videoio -I /home/a6000/projects/haonandong/env/opencv/opencv331/include/ -L /home/a6000/projects/haonandong/env/opencv/opencv331/lib/

## tansfer path into UTM coordinate.
g++ -o utm2wgs84_um utm2wgs84_uavmvs.cpp -L[path_to_proj_lib] -lproj  -lboost_system -lboost_filesystem -I/usr/include/eigen3 -I[path_to_proj_include]