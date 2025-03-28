# bin_path $1
# data_path $2


# safe airspace generation
$1/generate_proxy_mesh $2/uranus_utm49n.ply $2/airspace.ply --min-distance=3.0

## where the altitude means the uav height response to the sea level. the elevation refers to the terrain height according to the sea level.
$1/generate-trajectory $2/airspace.ply $2/oblique.traj --altitude=120 --elevation=20 --angles=0 --forward-overlap=80 --side-overlap=80

$1/optimize_trajectory $2/oblique.traj $2/uranus_utm49n_mesh.ply $2/uranus_utm49n.ply $2/airspace.ply $2/oblique_opt.traj -m 10000 --max-distance=20.0 --min-distance=15.0

$1/interpolate-trajectory $2/oblique.traj $2/oblique.csv
$1/interpolate-trajectory $2/oblique_opt.traj $2/oblique_opt.csv

# for visualization
python3 $1/../../scripts/python/visualizeDJITraj.py -i $2/oblique.csv -p $2/uranus_utm49n.ply -t uavmvs
python3 $1/../../scripts/python/visualizeDJITraj.py -i $2/oblique_opt.csv -p $2/uranus_utm49n.ply -t uavmvs