/*
 * Copyright (C) 2017-2018, Nils Moehrle
 * All rights reserved.
 *
 * This software may be modified and distributed under the terms
 * of the BSD 3-Clause license. See the LICENSE.txt file for details.
 */

#ifndef STAT_STATISTICS_HEADER
#define STAT_STATISTICS_HEADER

#include <vector>
#include <tuple>

#include "defines.h"

#define SQR(x) ((x) * (x))

STAT_NAMESPACE_BEGIN

template <typename T>
std::pair<T, T>
moments(std::vector<T> const & vec) {
    static_assert(std::is_floating_point<T>::value,
        "Floating point type required");

    if (vec.size() == 0)
        throw std::runtime_error("Cannot compute moments of empty vector.");
    if (vec.size() == 1) return std::make_pair(vec[0], T(0));

    double sum = 0, sqsum = 0, k = vec[0];
    for (std::size_t i = 0; i < vec.size(); ++i) {
        T val = vec[i];
        sum += val - k;
        sqsum += SQR(val - k);
    }

    double n = vec.size();

    T mean = sum / n + k;
    T var = (sqsum - SQR(sum) / n) / (n - 1);

    return std::make_pair(mean, var);
}

STAT_NAMESPACE_END

#endif /* STAT_STATISTICS_HEADER */
