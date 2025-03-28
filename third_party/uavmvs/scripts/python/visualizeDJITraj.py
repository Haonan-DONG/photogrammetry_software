import open3d as o3d
import numpy as np
import argparse
import math

from scipy.spatial.transform import Rotation as R

# define hard code
WIDTH = 1920
HEIGHT = 1080
SKIP_NUM = 20
MAX_VISUALIZE_CODE = 40
# an random camera intrinsic matrix
intrinsics = np.array([
    [1.16962109e+03, 0.00000000e+00, 960.0, 0.00000000e+00],
    [0.00000000e+00, 1.16710510e+03, 540.0, 0.00000000e+00],
    [0.00000000e+00, 0.00000000e+00, 1.00000000e+00, 0.00000000e+00],
    [0.00000000e+00, 0.00000000e+00, 0.00000000e+00, 1.00000000e+00]
    ])

 
def quaternion2rot(quaternion):
    # xyzw
    r = R.from_quat(quaternion)
    rot = r.as_matrix()
    return rot

def euler2rotationmatrix(eular):
    r = R.from_euler('xyz', eular, degrees=True)
    rot = r.as_matrix()
    return rot

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


def trajectory_visualization(pose_path, pcd_path, type='uavmvs'):

    # decode the extrinsic
    extrinsics = []

    with open(pose_path,'r') as pose_file :    # xyzw
        lines = pose_file.readlines()
        if type == 'uavmvs':
            print("Using uavmvs")
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
                # r_c_w
                rot = quaternion2rot(np.array([qx, qy, qz, qw]))
                # according to the code.
                xyz = np.array([x, y, z]).reshape(1,-1).transpose()
                trans = np.matmul(-rot, xyz)   # t_c_w = -r_c_w * c_w_o
                extrinsic = np.concatenate([rot, trans], axis=1)
                extrinsic = np.concatenate([extrinsic, np.array([0,0,0,1]).reshape(1,-1)], axis=0)
                extrinsics.append(extrinsic)   # T_c_w
        elif type == "fc-planner":
            # fc-planner as robotic visualization: x roll, y pitch, z yaw as xyz sequence.
            print("Using fc-planner")
            for line in lines:
                elems = line.split(' ')
                elems_num = len(elems)
                xyz = []
                for i in range(elems_num):
                    if elems[i] == 'X:':
                       xyz.append(float(elems[i+1][:-1]))
                    elif elems[i] == "Y:":
                        xyz.append(float(elems[i+1][:-1]))
                    elif elems[i] == "Z:":
                        xyz.append(float(elems[i+1][:-1]))
                    elif elems[i] == "PITCH:":
                        pitch = float(elems[i+1][:-1])*180.0/math.pi
                        pitch = 0 - (pitch - 90)
                    elif elems[i] == "YAW:":
                        yaw = float(elems[i+1][:-1])*180.0/math.pi

                euler_zyx = np.array([0.0, pitch, yaw])
                rot = euler2rotationmatrix(euler_zyx) # r_w_c
                trans = np.array(xyz).reshape(3, 1) # t_w_c
                extrinsic = np.concatenate([rot, trans], axis=1)
                extrinsic = np.concatenate([extrinsic, np.array([0,0,0,1]).reshape(1,-1)], axis=0)
                extrinsic = np.linalg.inv(extrinsic)
                extrinsics.append(extrinsic)   # T_c_w

        else:
            print("Error: Type Not Impl.")
            return

    frustrum_num = len(extrinsics)

    rainbow_colors = [
            (1, 0, 0),
            (0, 1, 0),
            (0, 0, 1),
        ]

    color_result = interpolate_colors(rainbow_colors, frustrum_num)

    # load a scene point cloud
    scene = o3d.io.read_point_cloud(pcd_path)

    # The x, y, z axis will be rendered as red, green, and blue arrows respectively.
    coor = o3d.geometry.TriangleMesh.create_coordinate_frame(size=20, origin=[0,0,0])    

    vizualizer = o3d.visualization.Visualizer()
    vizualizer.create_window(width=WIDTH, height=HEIGHT)

    vizualizer.add_geometry(scene)
    vizualizer.add_geometry(coor)


    for i in range(frustrum_num):
        if(frustrum_num > MAX_VISUALIZE_CODE):
            if(not i%SKIP_NUM):
                cameraLines = o3d.geometry.LineSet.create_camera_visualization(view_width_px=WIDTH, 
                                                                                view_height_px=HEIGHT, 
                                                                                intrinsic=intrinsics[:3,:3], 
                                                                                extrinsic=extrinsics[i], 
                                                                                scale=1.0)
                cameraLines.colors = o3d.utility.Vector3dVector(np.tile(color_result[i], (8, 1)))
                vizualizer.add_geometry(cameraLines)
        else:
            cameraLines = o3d.geometry.LineSet.create_camera_visualization(view_width_px=WIDTH, 
                                                                                view_height_px=HEIGHT, 
                                                                                intrinsic=intrinsics[:3,:3], 
                                                                                extrinsic=extrinsics[i], 
                                                                                scale=1.0)
            cameraLines.colors = o3d.utility.Vector3dVector(np.tile(color_result[i], (8, 1)))
            vizualizer.add_geometry(cameraLines)

    vizualizer.run()
    vizualizer.destroy_window()


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Generate DJI trajectory")
    parser.add_argument('-i', '--input', type=str, help='input trajectory file', required=True)
    parser.add_argument('-p', '--point', type=str, help='input point cloud', required=True)
    parser.add_argument('-t', '--type', type=str, help='trajectory file type: uavmvs, fc-planner', required=True, default='uavmvs')

    args = parser.parse_args()

    trajectory_visualization(args.input, args.point, args.type)