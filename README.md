# Photogrammetry Software
This repo mainly includes basic module for photogrammetry based on unmanned aerial vehicle. Important features include:
- UAV Path Planing
- Structure from Motion for Pose Estimation
- Multi-View Stereo for Dense Reconstruction
- Texture Mapping
- Rendering

## Pre-requisite
The code is tested on a Linux machine of Ubuntu 22.04 with RTX 6000 Ada. \
CUDA 11.8 \
Eigen 3.4.0 \
Ceres 2.0.0 \
CGAL 6.0.1


## How to use
```shell
# get the mission planning software
git clone https://github.com/Haonan-DONG/photogrammetry_software.git --recursive

## compile the third library mve
cd mve
make -j

## compile the root
cmake .. -DMVE_ROOT=../third_party/uavmvs/elibs/mve/
make -j

## path planning
bash shell/mission_plan.sh

# get the rgb_reconstruction
## compile colmap 
cd third_party/colmap
mkdir build
cd build
### here should change to your own cuda_architecture
cmake .. -GNinja -DCMAKE_CUDA_ARCHITECTURES=89
ninja

## compile openMVS
cd third_party/openMVS
mkdir bin && cd bin
cmake -DVCG_ROOT=[VCG_REPO_PATH] -DCMAKE_CUDA_ARCHITECTURES=89 -DCGAL_DIR=[CGAL_INSTALL_PATH] ..

cd scripts/shell
bash rgb_reconstruction [path_to_third_party] [path_to_data]
```
## Data and Run
### Mission Plan
The demo data is uploaded into [baidu disk, psw:7z9n](https://pan.baidu.com/s/1E1aecb8SpcAujOZ3HdEazg?pwd=7z9n), After running the mission_plan shell, the path will be visualized as follows:
![mission_plan_result](doc/mission_plan.png)

### RGB Reconstrcution
We provide a sample data in [baidu disk](https://pan.baidu.com/s/1Ekx5msUdmoQynWi4C12Fdw) from DTU datasets and the password is uts5. For custom data, he data format should be like:
```shell
---Project
    ---images
        ---A.png
        ---B.png
```


## TODO
### Tag 1.0
- [X] Add Mission planning code for DJI platform.
    - [X] Change uavmvs in a cmake lib
        - [X] Add MVE as the sfm basic lib
    - [X] Test the ndair and oblique path planning
    - [X] Test the optimized path planning
- [X] Released Pipeline for COLMAP for SfM.
- [X] Add openMVS as a library. From rgb input into textured mesh.

### Feature: suit large-scale dataset
- [ ] For large-scale dataset, incoorperate parallel-sfm module

### Feature: Lite Version
- [ ] Add lite version to generate the real-time orthorectified image.
    - [ ] Add GPS info from the exiv file.

### Feature: Add mesh refine by line constrain
- [ ] Add Mesh refine module by line constrain.

## Acknowledgements
- [uavmvs](https://github.com/nmoehrle/uavmvs)
- [COLMAP](https://github.com/colmap/colmap)
- [OpenMVS](https://github.com/cdcseacave/openMVS)
- [Poisson Reconstruction](https://www.cs.jhu.edu/~misha/Code/PoissonRecon/Version13.8/)
- [Meshlab](https://github.com/cnr-isti-vclab/meshlab)
- [OpenREALM](https://github.com/laxnpander/OpenREALM.git)
- [CGAL](https://github.com/CGAL/cgal.git)