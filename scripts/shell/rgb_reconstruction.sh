# $1 requires the third_party path
# $2 requires the absolute path.
rm -rf $2/sfm $2/mvs $2/mesh $2/data.db

# Feature Extraction and Match
echo "Feature Extracting..."
CUDA_VISIBLE_DEVICES=0  $1/colmap/build/src/colmap/exe/colmap feature_extractor --image_path $2/images/ --database_path $2/data.db
echo "Feature Extraction Done"

echo "Feature Matching..."
CUDA_VISIBLE_DEVICES=0 $1/colmap/build/src/colmap/exe/colmap exhaustive_matcher --database_path $2/data.db
echo "Feature Match Done"

# Structure from Motion
echo "Mapping..."
$1/colmap/build/src/colmap/exe/colmap mapper --image_path $2/images/ --database_path $2/data.db --output_path $2/
echo "Mapping Done."

# Undistortion
mv $2/0 $2/sparse
mkdir $2/sfm
echo "Undistorting..."
$1/colmap/build/src/colmap/exe/colmap image_undistorter --image_path $2/images/ --input_path $2/sparse/ --output_path $2/sfm
mv $2/sparse $2/sfm/sparse_radial
mv $2/data.db $2/sfm
echo "Undistortion Done"

# transfer into openmvs
cd $2/sfm
mkdir $2/mvs/
$1/openMVS/bin/bin/InterfaceCOLMAP -i $2/sfm/ -o $2/mvs/scene.mvs --image-folder images/

#Dense Reconstruction
cd $2/mvs
echo "Multiview Stereoing..."
CUDA_VISIBLE_DEVICES=0 $1/openMVS/bin/bin/DensifyPointCloud -i $2/mvs/scene.mvs -o $2/mvs/scene.ply
echo "Multiview Stereo Done"

# Mesh Reconstruction
mkdir $2/mesh
cd $2/mesh
echo "Meshing..."
CUDA_VISIBLE_DEVICES=0 $1/openMVS/bin/bin/ReconstructMesh -i $2/mvs/scene.mvs -o $2/mesh/scene_mesh.ply
CUDA_VISIBLE_DEVICES=0 $1/openMVS/bin/bin/RefineMesh -i $2/mvs/scene.mvs -m $2/mesh/scene_mesh.ply -o $2/mesh/scene_mesh_refined.ply
# Texture Mapping
CUDA_VISIBLE_DEVICES=0 $1/openMVS/bin/bin/TextureMesh -i $2/mvs/scene.mvs -m $2/mesh/scene_mesh_refined.ply -o $2/mesh/scene_textured.ply --export-type ply
echo "Mesh Reconstruction and Texturing Done"

echo "Done Reconstruction."