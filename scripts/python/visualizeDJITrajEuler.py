import open3d as o3d
import numpy as np
import sys

from scipy.spatial.transform import Rotation as R

def quaternion2euler(quaternion):
    # xyzw
    r = R.from_quat(quaternion)
    euler = r.as_euler('zyx', degrees=True)
    return euler

def euler2rotationmatrix(eular):
    # xyzw
    r = R.from_euler('zyx', eular, degrees=True)
    rot = r.as_matrix()
    return rot



WIDTH = 1280
HEIGHT = 720

pcd_path = sys.argv[1]
pose_path = sys.argv[2]

# an random camera intrinsic matrix
intrinsics = np.array([
    [1.16962109e+03, 0.00000000e+00, 6.46295044e+02, 0.00000000e+00],
    [0.00000000e+00, 1.16710510e+03, 4.89927032e+02, 0.00000000e+00],
    [0.00000000e+00, 0.00000000e+00, 1.00000000e+00, 0.00000000e+00],
    [0.00000000e+00, 0.00000000e+00, 0.00000000e+00, 1.00000000e+00]
    ])

# load a scene point cloud
scene = o3d.io.read_point_cloud(pcd_path)

# 可视化坐标轴. The x, y, z axis will be rendered as red, green, and blue arrows respectively.
coor = o3d.geometry.TriangleMesh.create_coordinate_frame(size=10, origin=[0,0,0])    

vizualizer = o3d.visualization.Visualizer()
vizualizer.create_window(width=WIDTH, height=HEIGHT)

vizualizer.add_geometry(scene)
vizualizer.add_geometry(coor)

def interpolate_colors(color_list, num_points):
    """
    对多个颜色进行线性差值
    :param color_list: 颜色列表，每个颜色为 RGB 元组
    :param num_points: 观测点数量
    :return: 差值后的颜色值数组
    """
    # 创建一个空的数组来存储插值结果
    interpolated_colors = []
    
    # 对每对颜色进行插值
    for i in range(len(color_list) - 1):
        start_color = np.array(color_list[i])
        end_color = np.array(color_list[i + 1])
        # 生成从 start_color 到 end_color 的插值
        colors = np.linspace(start_color, end_color, num_points)
        interpolated_colors.append(colors)
    
    # 将所有插值结果合并为一个数组
    return np.vstack(interpolated_colors)

extrinsics = []

with open(pose_path,'r') as pose_file :
    lines = pose_file.readlines()
    for line in lines: 
        if('x,y,z,qw,qx,qy,qz,key' in line):
            continue
        elems = line.split(',')
        x = float(elems[0])
        y = float(elems[1])
        z = float(elems[2])
        qw = float(elems[3])
        qx = float(elems[4])
        qy = float(elems[5])
        qz = float(elems[6])
        euler_zyx = quaternion2euler(np.array([qx, qy, qz, qw]))
        print(euler_zyx)

        rot = euler2rotationmatrix(euler_zyx)
        xyz = np.array([x, y, z]).reshape(1,-1).transpose()
        xyz_c = np.matmul(-rot, xyz)  # warning: not right?
        extrinsic = np.concatenate([rot, xyz_c], axis=1)
        extrinsic = np.concatenate([extrinsic, np.array([0,0,0,1]).reshape(1,-1)], axis=0)

        extrinsics.append(extrinsic)
        
frustrum_num = len(extrinsics)


rainbow_colors = [
        (1, 0, 0),    # 红色
        (0, 1, 0),    # 绿色
        (0, 0, 1),    # 蓝色
    ]

color_result = interpolate_colors(rainbow_colors, frustrum_num)


for i in range(frustrum_num):
    cameraLines = o3d.geometry.LineSet.create_camera_visualization(view_width_px=WIDTH, view_height_px=HEIGHT, intrinsic=intrinsics[:3,:3], extrinsic=extrinsics[i])
    cameraLines.colors = o3d.utility.Vector3dVector(np.tile(color_result[i], (8, 1)))
    vizualizer.add_geometry(cameraLines)


vizualizer.run()
vizualizer.destroy_window()

