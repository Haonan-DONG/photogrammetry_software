g++ -o add_gps add_gps.cpp -lexiv2 -lboost_system -lboost_filesystem -I /usr/include/eigen3/ -lopencv_core -lopencv_imgcodecs -lopencv_highgui -lopencv_videoio -I /home/a6000/projects/haonandong/env/opencv/opencv331/include/ -L /home/a6000/projects/haonandong/env/opencv/opencv331/lib/

g++ -o export_colmap  -g export_colmap_gps.cpp -lexiv2 -lboost_system -lboost_filesystem
