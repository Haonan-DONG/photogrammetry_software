#define ACCEPT_USE_OF_DEPRECATED_PROJ_API_H

#include <iostream>
#include <iomanip>
#include <vector>
#include <fstream>

#include <proj.h>
#include <proj_api.h>

#include <Eigen/Core>
#include <Eigen/Dense>

#include <boost/algorithm/string.hpp>

Eigen::Vector3d transferUTM2WGS84(double easting, double northing, double altitude)
{
    const char *wgs84 = "+proj=longlat +datum=WGS84 +no_defs "; // EPSG:32649
    const char *utm_crs = "+proj=utm +zone=49 +ellps=WGS84 +units=m +no_defs";
    projPJ m_pj_wgs84 = pj_init_plus(wgs84);
    projPJ m_pj_utm = pj_init_plus(utm_crs);

    pj_transform(m_pj_utm, m_pj_wgs84, 1, 1, &easting, &northing, nullptr);

    double longitude = easting * RAD_TO_DEG;
    double latitude = northing * RAD_TO_DEG;

    return Eigen::Vector3d(longitude, latitude, altitude);
}

void stringSplit(const std::string &str, const char &delimiter, std::vector<std::string> &splited_strs)
{

    boost::split(splited_strs, str, boost::is_any_of(std::string(1, delimiter)));
}

int readTrajUTM(const std::string &file_path, std::vector<Eigen::Vector3d> &utm_ps, std::vector<Eigen::Quaterniond> &utm_qs)
{
    std::ifstream file(file_path);

    if (!file.is_open())
    {
        std::cerr << "Error: Could not open the file " << file_path << std::endl;
        return false;
    }

    std::string line;
    std::cout << "Start to reading UTM coordinate from file." << std::endl;
    while (std::getline(file, line))
    {
        if (line.find("x,y,z,qw,qx,qy,qz,key") != std::string::npos)
        {
            continue;
        }

        std::cout << "Reading: " << line << std::endl;

        std::vector<std::string> splited_strs;
        stringSplit(line, ',', splited_strs);

        Eigen::Vector3d utm_p;
        Eigen::Quaterniond utm_q;

        // local shift to wgs84:32649
        utm_p[0] = std::atof(splited_strs[0].c_str()) + 798600.0;
        utm_p[1] = std::atof(splited_strs[1].c_str()) + 2516300.0;
        utm_p[2] = std::atof(splited_strs[2].c_str());

        utm_ps.push_back(utm_p);

        utm_q.w() = std::atof(splited_strs[3].c_str());
        utm_q.x() = std::atof(splited_strs[4].c_str());
        utm_q.y() = std::atof(splited_strs[5].c_str());
        utm_q.z() = std::atof(splited_strs[6].c_str());

        utm_qs.push_back(utm_q);
    }

    file.close();

    return true;
}

int main(int argc, char **argv)
{
    std::string input_traj_path = argv[1];
    std::string output_root_path = argv[2];

    std::vector<Eigen::Vector3d> utm_ps;
    std::vector<Eigen::Quaterniond> utm_qs;
    if (!readTrajUTM(input_traj_path, utm_ps, utm_qs))
    {
        std::cerr << "Not reading valid utm coords." << std::endl;
    }

    std::ofstream wgs84_traj_out(output_root_path + "/out_wgs84.txt");

    for (int i = 0; i < utm_ps.size(); i++)
    {
        Eigen::Vector3d WGS84_coords = transferUTM2WGS84(utm_ps[i](0), utm_ps[i](1), utm_ps[i](2));
        wgs84_traj_out << std::fixed << std::setprecision(10) << WGS84_coords(0) << "," << std::fixed << std::setprecision(10) << WGS84_coords(1) << "," << std::fixed << std::setprecision(10) << WGS84_coords(2) << "," << std::fixed << std::setprecision(10) << utm_qs[i].w() << "," << std::fixed << std::setprecision(10) << utm_qs[i].x() << "," << std::fixed << std::setprecision(10) << utm_qs[i].y() << "," << std::fixed << std::setprecision(10) << utm_qs[i].z() << std::endl;
    }

    wgs84_traj_out.close();

    return true;
}