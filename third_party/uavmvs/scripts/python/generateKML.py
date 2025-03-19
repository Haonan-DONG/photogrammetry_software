from lxml import etree
import argparse
import numpy as np
from scipy.spatial.transform import Rotation as R
from datetime import datetime
import math


MAX_PITCH_DEG = 35
MIN_PITCH_DEG = -90

def quaternion2euler(quaternion):
    # xyzw
    r = R.from_quat(quaternion)
    euler = r.as_euler('zyx', degrees=True)
    return euler

def quaternion2rot(quaternion):
    # xyzw
    r = R.from_quat(quaternion)
    rot = r.as_matrix()
    return rot



def load_traj(txt_file, filetype):
    traj = {}
    with open(txt_file, 'r') as file:
        lin_num = 0
        if filetype == "uavmvs":
            print("Using uavmvs")
            for line in file:
                xyzqwxyz = line.split(",")

                xyz_w_o = xyzqwxyz[:3]
                x_o = float(xyz_w_o[0])
                y_o = float(xyz_w_o[1])
                z_o = float(xyz_w_o[2])

                qwxyz = xyzqwxyz[3:]
                qw = float(qwxyz[0])
                qx = float(qwxyz[1])
                qy = float(qwxyz[2])
                qz = float(qwxyz[3])
                # r_c_w
                rot = quaternion2rot(np.array([qx, qy, qz, qw]))

                # calculate trans
                trans = np.matmul(-rot, np.array([x_o, y_o, z_o]).reshape(-1, 1))
                euler_zyx = quaternion2euler(np.array([qx, qy, qz, qw]))

                # suit DJI
                ## if pitch is smaller than 0, then the flight shoule be transformed 180 degree.
                ## DJI yaw range is [-180, 180]
                if euler_zyx[2] < 0:
                    ## change yaw
                    euler_zyx[0] += 180 * (euler_zyx[0] / abs(euler_zyx[0]))
                    if(euler_zyx[0] > 180):
                        euler_zyx[0] = euler_zyx[0] - 360
                    elif(euler_zyx[0]< -180):
                        euler_zyx[0] = euler_zyx[0] + 360

                    ## change pitch
                    euler_zyx[2] = -euler_zyx[2]

                euler_zyx[2] = 0 - (euler_zyx[2] - 90)

                if(euler_zyx[2] > MAX_PITCH_DEG or euler_zyx[2] < MIN_PITCH_DEG):
                    print("Warning: angle in " + str(lin_num) + " is not valid.")

                traj[str(lin_num)] = {'x': -trans[0][0], 'y': trans[1][0], 'z': trans[2][0],
                                         "roll": euler_zyx[1], "pitch": euler_zyx[2], "yaw" : euler_zyx[0]}
                lin_num+=1
        else:
            print("Using fc-planner")
            for line in file:
                elems = line.split(',')
                xyz = []
                xyz.append(float(elems[0]))
                xyz.append(float(elems[1]))
                xyz.append(float(elems[2]))
                # suit DJI
                ## if pitch is negative.
                ## DJI NEU , FC-PLANNER XYZ AND ANTI-CLOCKWISE
                pitch = float(elems[4])*180.0/math.pi
                yaw = 90.0 - float(elems[5])*180.0/math.pi

                if(yaw > 180.0):
                    yaw -= 360.0
                elif(yaw < -180.0):
                    yaw += 360.0

                    
                if(pitch > MAX_PITCH_DEG or pitch < MIN_PITCH_DEG):
                    print("Warning: angle in " + str(lin_num) + " is not valid.")
                traj[str(lin_num)] = {'x': xyz[0], 'y': xyz[1], 'z': xyz[2],
                                     "roll": 0, "pitch": pitch, "yaw" : yaw}
                lin_num+=1


    return traj

def generate_kml(input_filepath, filetype):
    # create root
    kml = etree.Element(
        '{http://www.opengis.net/kml/2.2}kml',
        nsmap={
            None: 'http://www.opengis.net/kml/2.2',  # default namespace
            'wpml': 'http://www.dji.com/wpmz/1.0.6'  # namespace wpml
        }
    )
    
    # create Document
    document = etree.SubElement(kml, '{http://www.opengis.net/kml/2.2}Document')

    now = datetime.now()
    timestamp = int(now.timestamp())
    print("current time stamp", timestamp)

    formatted_time = now.strftime("%Y-%m-%d-%H:%M:%S")

    # Add subelement
    etree.SubElement(document, 'name').text = 'optimized_view_uav_planning_' + formatted_time
    etree.SubElement(document, '{http://www.dji.com/wpmz/1.0.6}createTime').text = str(timestamp)
    
    mission_config = etree.SubElement(document, '{http://www.dji.com/wpmz/1.0.6}missionConfig')
    etree.SubElement(mission_config, '{http://www.dji.com/wpmz/1.0.6}flyToWaylineMode').text = 'safely'
    etree.SubElement(mission_config, '{http://www.dji.com/wpmz/1.0.6}finishAction').text = 'goHome'
    etree.SubElement(mission_config, '{http://www.dji.com/wpmz/1.0.6}exitOnRCLost').text = 'executeLostAction'
    etree.SubElement(mission_config, '{http://www.dji.com/wpmz/1.0.6}executeRCLostAction').text = 'goBack'
    etree.SubElement(mission_config, '{http://www.dji.com/wpmz/1.0.6}takeOffSecurityHeight').text = '20'
    etree.SubElement(mission_config, '{http://www.dji.com/wpmz/1.0.6}globalTransitionalSpeed').text = '9'
    etree.SubElement(mission_config, '{http://www.dji.com/wpmz/1.0.6}globalRTHHeight').text = '120'

    # set info for drone.
    drone_info = etree.SubElement(mission_config, '{http://www.dji.com/wpmz/1.0.6}droneInfo')
    etree.SubElement(drone_info, '{http://www.dji.com/wpmz/1.0.6}droneEnumValue').text = '77'
    etree.SubElement(drone_info, '{http://www.dji.com/wpmz/1.0.6}droneSubEnumValue').text = '0'
    
    # set info for payload info
    payload_info = etree.SubElement(mission_config, '{http://www.dji.com/wpmz/1.0.6}payloadInfo')
    etree.SubElement(payload_info, '{http://www.dji.com/wpmz/1.0.6}payloadEnumValue').text = '66'
    etree.SubElement(payload_info, '{http://www.dji.com/wpmz/1.0.6}payloadPositionIndex').text = '0'

    # set up path folder
    folder = etree.SubElement(document, 'Folder')
    etree.SubElement(folder, '{http://www.dji.com/wpmz/1.0.6}templateType').text = 'waypoint'
    etree.SubElement(folder, '{http://www.dji.com/wpmz/1.0.6}templateId').text = '0'
    etree.SubElement(folder, '{http://www.dji.com/wpmz/1.0.6}autoFlightSpeed').text = '8'   # set the speed as 8m/s
    etree.SubElement(folder, '{http://www.dji.com/wpmz/1.0.6}gimbalPitchMode').text = 'usePointSetting'
    etree.SubElement(folder, '{http://www.dji.com/wpmz/1.0.6}globalWaypointTurnMode').text = 'toPointAndPassWithContinuityCurvature'

    ## set up coordinate system.
    wgs84_sys = etree.SubElement(folder, '{http://www.dji.com/wpmz/1.0.6}waylineCoordinateSysParam')
    etree.SubElement(wgs84_sys, '{http://www.dji.com/wpmz/1.0.6}coordinateMode').text = 'WGS84'
    etree.SubElement(wgs84_sys, '{http://www.dji.com/wpmz/1.0.6}heightMode').text = 'relativeToStartPoint'

    ## set up for payloadparams.
    payload_param = etree.SubElement(folder, '{http://www.dji.com/wpmz/1.0.6}payloadParam')
    etree.SubElement(payload_param, '{http://www.dji.com/wpmz/1.0.6}dewarpingEnable').text = '0'

    # make place mark kml
    make_palce_mark_kml(folder, input_filepath, filetype)

    return kml

def make_palce_mark_kml(folder, input_filepath, filetype):
    print('Adding place mark')
    traj_info = load_traj(input_filepath, filetype)
    traj_num = len(traj_info)
    print('Done loading wgs84 traj with ' + str(traj_num) + " points.")

    for i in range(traj_num):
        # set placemark
        placemark = etree.SubElement(folder, 'Placemark')        
        etree.SubElement(placemark, '{http://www.dji.com/wpmz/1.0.6}index').text = str(i)
        etree.SubElement(placemark, '{http://www.dji.com/wpmz/1.0.6}useGlobalHeight').text = '0'
        etree.SubElement(placemark, '{http://www.dji.com/wpmz/1.0.6}useGlobalSpeed').text = '1'
        etree.SubElement(placemark, '{http://www.dji.com/wpmz/1.0.6}useGlobalTurnParam').text = '1'


        ## set point
        point = etree.SubElement(placemark, 'Point')
        etree.SubElement(point, 'coordinates').text = str(traj_info[str(i)]['x']) + ',' + str(traj_info[str(i)]['y'])
        etree.SubElement(placemark, '{http://www.dji.com/wpmz/1.0.6}height').text = str(traj_info[str(i)]['z'])

        ## set waypointheading
        waypointheading_param = etree.SubElement(placemark, '{http://www.dji.com/wpmz/1.0.6}waypointHeadingParam')
        etree.SubElement(waypointheading_param, '{http://www.dji.com/wpmz/1.0.6}waypointHeadingMode').text = 'smoothTransition'
        etree.SubElement(waypointheading_param, '{http://www.dji.com/wpmz/1.0.6}waypointHeadingAngle').text = str(traj_info[str(i)]['yaw'])
        etree.SubElement(waypointheading_param, '{http://www.dji.com/wpmz/1.0.6}waypointHeadingPathMode').text = 'followBadArc'

        ## set gimbal pose
        etree.SubElement(placemark, '{http://www.dji.com/wpmz/1.0.6}gimbalPitchAngle').text = str(traj_info[str(i)]['pitch'])

        ## set actiongroup
        ## currently, only support take photo
        action_group = etree.SubElement(placemark, '{http://www.dji.com/wpmz/1.0.6}actionGroup')
        etree.SubElement(action_group, '{http://www.dji.com/wpmz/1.0.6}actionGroupId').text = '0'
        etree.SubElement(action_group, '{http://www.dji.com/wpmz/1.0.6}actionGroupStartIndex').text = str(i)
        etree.SubElement(action_group, '{http://www.dji.com/wpmz/1.0.6}actionGroupEndIndex').text = str(i)
        etree.SubElement(action_group, '{http://www.dji.com/wpmz/1.0.6}actionGroupMode').text = 'sequence'
        ### add action trigger
        action_group_trigger = etree.SubElement(action_group, '{http://www.dji.com/wpmz/1.0.6}actionTrigger')
        etree.SubElement(action_group_trigger, '{http://www.dji.com/wpmz/1.0.6}actionTriggerType').text = 'reachPoint'
        ### add action for taking photo
        action = etree.SubElement(action_group, '{http://www.dji.com/wpmz/1.0.6}action')
        etree.SubElement(action, '{http://www.dji.com/wpmz/1.0.6}actionId').text = '0'
        etree.SubElement(action, '{http://www.dji.com/wpmz/1.0.6}actionActuatorFunc').text = 'takePhoto'
        
    print("Done saving all placemarks")

def save_path_kml(kml, output_filepath):
    # write xml
    tree = etree.ElementTree(kml)
    tree.write(output_filepath, encoding='UTF-8', xml_declaration=True, pretty_print=True)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Generate DJI trajectory")
    parser.add_argument('-i', '--input', type=str, help='input xyz qwxyz file in WGS84', required=True)
    parser.add_argument('-o', '--output', type=str, help='output wmpl file', required=True)
    parser.add_argument('-t', '--type', type=str, help='trajectory type', required=True)

    args = parser.parse_args()

    kml = generate_kml(args.input, args.type)
    save_path_kml(kml, args.output)
    print("Done saving path kml in: " + args.output)