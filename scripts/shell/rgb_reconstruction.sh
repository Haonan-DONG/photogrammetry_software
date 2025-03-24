# $1 requires the absolute path.
rm -rf $1/sfm $1/mvs $1/mesh

# Feature Extraction and Match
third_party/colmap/build/src/exe/colmap feature_extractor --image_path $1/images/ --database_path $1/data.db
third_party/colmap/build/src/exe/colmap exhaustive_matcher --database_path $1/data.db

# Structure from Motion
third_party/colmap/build/src/exe/colmap mapper --image_path $1/images/ --database_path $1/data.db --output_path $1/

#Undistortion
mv $1/0 $1/sparse
mkdir $1/sfm
third_party/colmap/build/src/exe/colmap image_undistorter --image_path $1/images/ --input_path $1/sparse/ --output_path $1/sfm
mv $1/sparse $1/sfm/sparse_radial
mv $1/data.db $1/sfm

#transfer into openmvs
mkdir $1/mvs/
third_party/openMVS/make/bin/InterfaceCOLMAP -i $1/sfm/ -o $1/mvs/scene.mvs

#Dense Reconstruction
third_party/openMVS/make/bin/DensifyPointCloud -i $1/mvs/scene.mvs -o $1/mvs/scene.ply

# Mesh Reconstruction
mkdir $1/mesh/
third_party/openMVS/make/bin/ReconstructMesh -i $1/mvs/scene.mvs -o $1/mesh/scene_mesh.ply
third_party/openMVS/make/bin/RefineMesh -i $1/mesh/scene_mesh.mvs -o $1/mesh/scene_mesh_refined.ply
# Texture Mapping
third_party/openMVS/make/bin/TextureMesh -i $1/mesh/scene_mesh_refined.mvs -o $1/mesh/scene_textured.ply --export-type ply

rm *dmap *log
echo "Done Reconstruction."