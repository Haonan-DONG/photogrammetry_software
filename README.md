# Photogrammetry Software
## Purpose
- A handy pipeline to make a textured mesh from rgb images (currently) by the traditional methods.
- Reproduce the latest methods.

## How to use
```shell
# get the mission planning software
git clone --recursive https://github.com/nmoehrle/uavmvs.git

## compile the mve and mvst lib
cd mve
make -j

cd mvs-texturing
mkdir build
cmake ..  && make -j

cmake .. -DMVE_ROOT=../third_party/uavmvs/elibs/mve/ -DMVST_ROOT=../third_party/uavmvs/elibs/mvs-texturing/
```

## TODO
- [X] Add Mission planning code for DJI platform.
    - [ ] Change uavmvs in a cmake lib.
- [X] Released Pipeline for COLMAP for SfM.
- [ ] Add openMVS as a library. From rgb input into textured mesh.


## Acknowledgements
- [uavmvs](https://github.com/nmoehrle/uavmvs)
- [COLMAP](https://github.com/colmap/colmap)
- [OpenMVS](https://github.com/cdcseacave/openMVS)
- [Poisson Reconstruction](https://www.cs.jhu.edu/~misha/Code/PoissonRecon/Version13.8/)
- [Meshlab](https://github.com/cnr-isti-vclab/meshlab)