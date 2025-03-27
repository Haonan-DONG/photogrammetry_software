# $1 requires the third_party path
# $2 requires the absolute path.
rm -rf $2/sfm $2/mvs $2/mesh

# Feature Extraction and Match
$1/colmap/build/src/colmap/exe/colmap feature_extractor --image_path $2/images/ --database_path $2/data.db
$1/colmap/build/src/colmap/exe/colmap exhaustive_matcher --database_path $2/data.db

# Structure from Motion
$1/colmap/build/src/colmap/exe/colmap mapper --image_path $2/images/ --database_path $2/data.db --output_path $2/

#Undistortion
mv $2/0 $2/sparse
mkdir $2/sfm
$1/colmap/build/src/colmap/exe/colmap image_undistorter --image_path $2/images/ --input_path $2/sparse/ --output_path $2/sfm
mv $2/sparse $2/sfm/sparse_radial
mv $2/data.db $2/sfm

#transfer into openmvs
mkdir $2/mvs/
$1/openMVS/bin/bin/InterfaceCOLMAP -i $2/sfm/ -o $2/mvs/scene.mvs

#Dense Reconstruction
$1/openMVS/bin/bin/DensifyPointCloud -i $2/mvs/scene.mvs -o $2/mvs/scene.ply

# Mesh Reconstruction
mkdir $2/mesh/
$1/openMVS/bin/bin/ReconstructMesh -i $2/mvs/scene.mvs -o $2/mesh/scene_mesh.ply
$1/openMVS/bin/bin/RefineMesh -i $2/mesh/scene_mesh.mvs -o $2/mesh/scene_mesh_refined.ply
# Texture Mapping
$1/openMVS/bin/bin/TextureMesh -i $2/mesh/scene_mesh_refined.mvs -o $2/mesh/scene_textured.ply --export-type ply

rm *dmap *log
echo "Done Reconstruction."