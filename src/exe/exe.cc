#include <cstdlib>
#include <iostream>

#include <colmap/util/option_manager.h>
#include <colmap/util/string.h>
#include <colmap/exe/feature.h>

int main(int argc, char **argv)
{
    // colmap::InitializeGlog(argv);

    colmap::RunFeatureExtractor(argc, argv);

    return EXIT_SUCCESS;
}