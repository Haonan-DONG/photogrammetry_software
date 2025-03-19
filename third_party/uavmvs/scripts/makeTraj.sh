#!/bin/bash
set -e
#Focal: 15/17.3=0.867
aspect=0.66 #4000/6000 camera resolution
focal=0.867
maxD=30
maxDR=35
minD=5
alt=15
elev=-15
f=80
s=80

#Set proper directories for your build!
binaries=$(cd /home/a6000/projects/haonandong/path_planning/uavmvs/build/release; pwd)
scripts=$(cd /home/a6000/projects/haonandong/path_planning/uavmvs/scripts; pwd)
mveapps=$(cd /home/a6000/projects/haonandong/path_planning/uavmvs/env/mve/apps; pwd)
export PATH=/bin:/usr/bin:$binaries:$scripts

root=$(pwd)
host=$(hostname)

#Create project name of experiment
project=/home/a6000/projects/haonandong/path_planning/uavmvs/experiment/

meshes=$project/meshes
models=$project/models
scenes=$project/scenes

mkdir $project
mkdir $meshes    
mkdir $models
mkdir $scenes
mkdir $scenes/nadir
mkdir $scenes/recon

    

# Setup folder structure
overlap_dir=$scenes/overlap-${f}-${s}
plan_dir=$overlap_dir/plan
nadir_dir=$overlap_dir/nadir
oblique_dir=$overlap_dir/oblique
nadir_opti_dir=$overlap_dir/nadir-opti
oblique_opti_dir=$overlap_dir/oblique-opti
oblique_view=oblique

mkdir $overlap_dir
mkdir $plan_dir

# Make Textured version of groundtruth mesh
# convert-mesh $data $meshes/mesh.ply
# generate_texture --resolution=45 -n 50 -f 1.6 $meshes/mesh.ply $models/model
    

  
#This takes as input the point cloud representing the proxy model
#Note: if you only have a mesh or it has many holes first convert to point cloud using this command:
generate_proxy_cloud gesox-mesh.ply gesox-cloud.ply --samples=25
generate_proxy_mesh $root/$scenes/recon/gesox-cloud.ply $root/$scenes/recon/gesox-mesh.ply
generate_proxy_mesh $root/$scenes/recon/gesox-cloud.ply $root/$scenes/recon/airspace.ply \
            --min-distance=3.0


cd $plan_dir

#Generate Trajectory calculates the estimated density of cameras desired for path planning. 
#Use this to control density of cameras. This should be controlled by adjusting alt and elev.
#The distance between elev and alt is used to calculate density of forward and side overlap. 
#You should only need to adjust elev to affect density. Alt should be higher then highest building.

generate-trajectory $root/$scenes/recon/gesox-mesh.ply oblique.traj \
             --altitude=$alt --elevation=$elev --angles=0 \
             --forward-overlap=$f --side-overlap=$s

optimize_trajectory oblique.traj $root/$scenes/recon/gesox-mesh.ply $root/$scenes/recon/gesox-cloud.ply \
             $root/$scenes/recon/airspace.ply oblique-opti.traj \
             -m 10000 --max-distance=$maxD --min-distance=$minD
       
shorten-trajectory oblique-opti.traj oblique-opti.traj

# This will visualize how good the reconstruction is estimated to be
evaluate_trajectory oblique-opti.traj $root/$meshes/mesh.ply $root/$scenes/recon/gesox-cloud.ply \
            --max-distance=$maxDR -r recon.ply

# This converts trajectory views to spline trajectory in csv format
         interpolate-trajectory oblique-opti.traj oblique_spline.csv
        

cd $root