#include <iostream>
#include <fstream>
#include <vector>
#include <string>
#include <iomanip>
#include <sstream>
#include <algorithm>

#include <exiv2/exiv2.hpp>

#include <Eigen/Core>
#include <Eigen/Dense>
#include <Eigen/Geometry>

#include <opencv2/opencv.hpp>

#include <boost/filesystem.hpp>
#include <boost/algorithm/string.hpp>

// hardcode
#define LAT_STRING_NUM 19
#define LONG_STRING_NUM 21
#define ALT_STRING_NUM 16
#define SKIP_IMAGE_NUM 30

// define ellipse parameter for GCJ02
#define ELLIPSE_A 6378245.0
#define ELLIPSE_EE 0.00669342162296594323
#define ELLIPSE_X_PI M_PI * 3000.0 / 180.0

struct GPSInfo
{
    double latitude_;
    double longitude_;
    double alt_;
    Eigen::Quaterniond q_;
};

void transfromLat(const double &x, const double &y, double &ret)
{
    ret = -100.0 + 2.0 * x + 3.0 * y + 0.2 * y * y + 0.1 * x * y + 0.2 * std::sqrt(std::abs(x));
    ret += (20.0 * std::sin(6.0 * x * M_PI) + 20.0 * std::sin(2.0 * x * M_PI)) * 2.0 / 3.0;
    ret += (20.0 * std::sin(y * M_PI) + 40.0 * std::sin(y / 3.0 * M_PI)) * 2.0 / 3.0;
    ret += (160.0 * std::sin(y / 12.0 * M_PI) + 320.0 * std::sin(y * M_PI / 30.0)) * 2.0 / 3.0;
}

void transfromLng(const double &x, const double &y, double &ret)
{
    ret = 300.0 + x + 2.0 * y + 0.1 * x * x + 0.1 * x * y + 0.1 * std::sqrt(std::abs(x));
    ret += (20.0 * std::sin(6.0 * x * M_PI) + 20.0 * std::sin(2.0 * x * M_PI)) * 2.0 / 3.0;
    ret += (20.0 * std::sin(x * M_PI) + 40.0 * std::sin(x / 3.0 * M_PI)) * 2.0 / 3.0;
    ret += (150.0 * std::sin(x / 12.0 * M_PI) + 300.0 * std::sin(x / 30.0 * M_PI)) * 2.0 / 3.0;
}

// WGS84 -> GCJ02
void WGS84ToGCJ02(const double &lat_in, const double &lng_in, double &lat_out, double &lng_out)
{
    double d_lat, d_lng;
    transfromLat(lng_in - 105.0, lat_in - 35.0, d_lat);
    transfromLng(lng_in - 105.0, lat_in - 35.0, d_lng);

    double lat_rad = lat_in / 180.0 * M_PI;
    double magic = std::sin(lat_rad);
    magic = 1 - ELLIPSE_EE * magic * magic;
    double sqrt_magic = std::sqrt(magic);
    d_lat = (d_lat * 180.0) / ((ELLIPSE_A * (1 - ELLIPSE_EE)) / (magic * sqrt_magic) * M_PI);
    d_lng = (d_lng * 180.0) / (ELLIPSE_A / sqrt_magic * std::cos(lat_rad) * M_PI);

    lat_out = lat_in + d_lat;
    lng_out = lng_in + d_lng;
}

void stringSplit(const std::string &str, const char &delimiter, std::vector<std::string> &splited_strs)
{

    // 使用 boost::split 进行字符串分割
    boost::split(splited_strs, str, boost::is_any_of(std::string(1, delimiter)));
}

void getDataXYZ(const std::string &str, double &gps_info)
{
    std::vector<std::string> split_result;
    stringSplit(str, ' ', split_result);
    gps_info = std::atof(split_result[1].c_str());
}

void getDataPose(const std::string &str, Eigen::Quaterniond &pose)
{
    Eigen::Vector3d eular_angle;
    std::vector<std::string> split_result;
    stringSplit(str, ' ', split_result);
    eular_angle[2] = std::atof(split_result[1].c_str());
    eular_angle[1] = std::atof(split_result[3].c_str());
    eular_angle[0] = std::atof(split_result[5].substr(0, split_result[5].size() - 1).c_str());

    pose = Eigen::AngleAxisd(eular_angle[0] / 180.0 * M_PI, Eigen::Vector3d::UnitX()) *
           Eigen::AngleAxisd(eular_angle[1] / 180.0 * M_PI, Eigen::Vector3d::UnitY()) *
           Eigen::AngleAxisd(eular_angle[2] / 180.0 * M_PI, Eigen::Vector3d::UnitZ());

    pose.normalize();
}

void readGPSFromFile(const std::string &gps_info_path, std::vector<GPSInfo> &gps_infos)
{
    std::ifstream file(gps_info_path); // 打开文件

    // 检查文件是否成功打开
    if (!file.is_open())
    {
        std::cerr << "Error: Could not open the file " << gps_info_path << std::endl;
        return;
    }

    std::string line;
    // 按行读取文件
    while (std::getline(file, line))
    {
        if (line.find("[iso") != std::string::npos)
        {
            GPSInfo gps_info;

            // Get XYZ
            std::string lat_str = line.substr(line.find("latitude: "), LAT_STRING_NUM);
            getDataXYZ(lat_str, gps_info.latitude_);

            std::string long_str = line.substr(line.find("longitude: "), LONG_STRING_NUM);
            getDataXYZ(long_str, gps_info.longitude_);

            std::string alt_str = line.substr(line.find("abs_alt: "), ALT_STRING_NUM);
            getDataXYZ(alt_str, gps_info.alt_);

            // Get Pose
            std::string pose_string = line.substr(line.find("gb_yaw: "));
            getDataPose(pose_string, gps_info.q_);

            // std::cout << std::fixed << std::setprecision(6) << gps_info.latitude_ << std::endl;
            // std::cout << std::fixed << std::setprecision(6) << gps_info.longitude_ << std::endl;
            // std::cout << std::fixed << std::setprecision(6) << gps_info.alt_ << std::endl;
            // std::cout << gps_info.q_.w() << "\t" << gps_info.q_.x() << "\t" << gps_info.q_.y() << "\t" << gps_info.q_.z() << "\t" << std::endl;

            // // transfer WGS84 into GCJ02
            // GPSInfo gps_info_gcj02;
            // WGS84ToGCJ02(gps_info.latitude_, gps_info.longitude_, gps_info_gcj02.latitude_, gps_info_gcj02.longitude_);
            // gps_info_gcj02.alt_ = gps_info.alt_;
            // gps_info_gcj02.q_ = gps_info.q_;

            gps_infos.push_back(gps_info);
        }
    }

    file.close(); // 关闭文件
}

void extractFrame(const std::string &video_path, const std::string &output_path)
{
    // 打开视频文件
    cv::VideoCapture cap(video_path);
    if (!cap.isOpened())
    {
        std::cerr << "Error: Could not open video file." << std::endl;
        return;
    }

    cv::Mat frame;
    int total_frame_num = static_cast<int>(cap.get(cv::CAP_PROP_FRAME_COUNT));
    int num_bit = std::to_string(total_frame_num).length() + 3;
    int file_num = 0;

    while (true)
    {
        cap >> frame;
        if (frame.empty())
        {
            break; // 如果读取到空帧，则停止
        }

        if (file_num % SKIP_IMAGE_NUM)
        {
            file_num++;
            continue;
        }

        if (!(file_num % 500))
            std::cout << "Processing " << file_num << std::endl;

        std::stringstream ss;
        ss << std::setfill('0') << std::setw(num_bit) << file_num;
        std::string filename = output_path + "/frame_" + ss.str() + ".jpg";
        cv::imwrite(filename, frame);
        std::cout << "Saved image: " << filename << std::endl;
        file_num++;
    }

    cap.release();
    std::cout << "All image frame saved, total num: " << total_frame_num << std::endl;
}
std::string toExifString(double d)
{
    char result[200];
    d *= 100;
    snprintf(result, sizeof(result), "%d/100", abs(static_cast<int>(d)));
    return result;
}

std::string toExifString(double d, bool bLat)
{
    const char *NS = d >= 0.0 ? "N" : "S";
    const char *EW = d >= 0.0 ? "E" : "W";
    const char *NSEW = bLat ? NS : EW;
    if (d < 0)
        d = -d;
    auto deg = static_cast<int>(d);
    d -= deg;
    d *= 60;
    auto min = static_cast<int>(d);
    d -= min;
    d *= 60;
    auto sec = static_cast<int>(d * 1000000);
    char result[200];
    snprintf(result, sizeof(result), "%d/1 %d/1 %d/1000000", deg, min, sec);
    return result;
}

void addGPSInfo(const std::string &image_path, const GPSInfo &gps_info)
{
    try
    {
        // 打开图像文件
        Exiv2::Image::AutoPtr image = Exiv2::ImageFactory::open(image_path);
        Exiv2::ExifData &exifData = image->exifData();

        exifData["Exif.GPSInfo.GPSLatitude"] = toExifString(gps_info.latitude_, true);
        exifData["Exif.GPSInfo.GPSLongitude"] = toExifString(gps_info.longitude_, false);
        exifData["Exif.GPSInfo.GPSAltitude"] = toExifString(gps_info.alt_); // 高度以厘米为单位

        exifData["Exif.GPSInfo.GPSLatitudeRef"] = (gps_info.latitude_ >= 0) ? "N" : "S";
        exifData["Exif.GPSInfo.GPSLongitudeRef"] = (gps_info.longitude_ >= 0) ? "E" : "W";
        exifData["Exif.GPSInfo.GPSAltitudeRef"] = (gps_info.alt_ >= 0) ? 0 : 1;
        // 0: above sea level, 1: below sea level

        image->writeMetadata();

        std::cout << "GPS information added successfully in: " << image_path << std::endl;
    }
    catch (const Exiv2::Error &e)
    {
        std::cerr << "Error: " << e.what() << std::endl;
    }
}

bool createDirectory(const std::string &dir_path)
{
    boost::filesystem::path dir(dir_path);

    // 检查目录是否存在
    if (boost::filesystem::exists(dir))
    {
        // 检查目录是否为空
        if (boost::filesystem::is_empty(dir))
        {
            std::cout << "Directory exists but is empty. Creating new files is allowed." << std::endl;
        }
        else
        {
            std::cout << "Directory exists and is not empty. Exiting." << std::endl;
            return false; // 目录存在且不为空，退出
        }
    }
    else
    {
        // 创建目录
        if (boost::filesystem::create_directory(dir))
        {
            std::cout << "Directory created: " << dir_path << std::endl;
        }
        else
        {
            std::cerr << "Error: Could not create directory." << std::endl;
            return false;
        }
    }

    return true;
}

int main(int argc, char **argv)
{
    std::string video_path = argv[1];
    std::string gps_path = argv[2];
    std::string output_path = argv[3];

    if (createDirectory(output_path))
    {
        std::cout << "Frames are extracted."
                  << std::endl;
        extractFrame(video_path, output_path);
    }

    // step 3: read gps info.
    std::vector<GPSInfo> gps_infos;
    readGPSFromFile(gps_path, gps_infos);

    std::cout << "Read " << gps_infos.size() << " gps infos." << std::endl;

    // step 4: write gps info
    std::vector<std::string> frame_paths;
    for (const auto &entry : boost::filesystem::directory_iterator(output_path))
    {
        if (boost::filesystem::is_regular_file(entry))
        {
            frame_paths.push_back(entry.path().filename().string());
        }
    }
    std::sort(frame_paths.begin(), frame_paths.end());

    if (gps_infos.size() != frame_paths.size())
    {
        std::cout << "Error: gps info num != frame num: " << gps_infos.size() << "\t" << frame_paths.size() << std::endl;
    }

    for (int i = 0; i < frame_paths.size(); i++)
    {
        addGPSInfo(output_path + "/" + frame_paths[i], gps_infos[i * SKIP_IMAGE_NUM]);
    }

    return 0;
}