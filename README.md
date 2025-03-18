# Photogrammetry Software
## Purpose
- A handy pipeline to make a textured mesh from rgb images (currently) by the traditional methods.
- Reproduce the latest methods.

## How to use
```shell
# Compile COLMAP and OpenMVS in the ACKNOWLEDGE into the directory "third_party", and run the following script.
bash rgb_reconstruction.sh $1   # $1 must be an absolute path.
```

## Data configuration
```
-- test
    -- images      --> Image and camera prior information.
        -- 00000000.jpg
        -- 00000001.jpg
        ...
        -- 00000333.jpg
    -- sfm         --> Undistorted images, poses and optimized intrinsics.
    -- mvs         --> Depth map and fused point cloud.
    -- mesh        --> Textured and un-textured mesh.
```
We provide a [sample data](https://pan.baidu.com/s/1Ekx5msUdmoQynWi4C12Fdw) in Baidu Disk from DTU datasets and the password is *uts5*.

## TODO
- [ ] Add Mission planning code for DJI platform.
- [X] Released Pipeline for COLMAP for SfM.
- [ ] Add openMVS as a library. From rgb input into textured mesh.

## Samples
- [X] DTU-scan1
- [ ] Scannet
- [ ] Eth3d

## Acknowledgements
- [COLMAP](https://github.com/colmap/colmap)
- [OpenMVS](https://github.com/cdcseacave/openMVS)
- [Poisson Reconstruction](https://www.cs.jhu.edu/~misha/Code/PoissonRecon/Version13.8/)
- [Meshlab](https://github.com/cnr-isti-vclab/meshlab)