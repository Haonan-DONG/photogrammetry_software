/*
 * Copyright (C) 2017-2018, Nils Moehrle
 * All rights reserved.
 *
 * This software may be modified and distributed under the terms
 * of the BSD 3-Clause license. See the LICENSE.txt file for details.
 */

#ifndef STAT_CORRELATIONS_HEADER
#define STAT_CORRELATIONS_HEADER

#include <algorithm>

#include "statistics.h"

STAT_NAMESPACE_BEGIN

template <typename T>
std::vector<std::size_t> rank(std::vector<T> const & vec) {
    std::vector<std::size_t> sidx(vec.size());
    std::iota(sidx.begin(), sidx.end(), 0);
    std::sort(sidx.begin(), sidx.end(), [&vec]
        (int r, int l) { return vec[r] < vec[l]; });
    std::vector<std::size_t> ret(vec.size());
    for (std::size_t i = 0; i < ret.size(); ++i) {
        ret[sidx[i]] = i;
    }
    return ret;
}

template <typename T>
std::vector<T> rankf(std::vector<T> x) {
    static_assert(std::is_floating_point<T>::value,
        "Floating point type required");

    std::vector<std::size_t> xrank = rank(x);
    std::sort(x.begin(), x.end());

    /* Compute floating rank for equal elements. */
    std::vector<T> xrankf(x.size());
    for (std::size_t i = 0, j = 1; j <= x.size(); ++j) {
        if (j < x.size() && x[i] == x[j]) continue;

        T rank = static_cast<T>(i + j - 1) / T(2.0);
        for (; i < j; ++i) {
            xrankf[i] = rank;
        }
    }

    for (std::size_t i = 0; i < x.size(); ++i) {
        x[i] = xrankf[xrank[i]];
    }

    return x;
}

template <typename T>
T pearson_correlation(std::vector<T> x, std::vector<T> y) {
    static_assert(std::is_floating_point<T>::value,
        "Floating point type required");

    T x_mean, x_var;
    std::tie(x_mean, x_var) = moments(x);
    T x_std = std::sqrt(x_var);

    T y_mean, y_var;
    std::tie(y_mean, y_var) = moments(y);
    T y_std = std::sqrt(y_var);

    std::size_t n = x.size();

    double sum = 0.0;
    for (std::size_t i = 0; i < n; ++i) {
        sum += ((x[i] - x_mean) / x_std) *
            ((y[i] - y_mean) / y_std);
    }

    return (1.0 / (n - 1)) * sum;
}

template <typename T>
T spearmans_rank_correlation(std::vector<T> const & x, std::vector<T> const & y) {
    if (x.size() != y.size()) throw;

    std::vector<T> xrankf = rankf(x);
    std::vector<T> yrankf = rankf(y);
    return pearson_correlation(xrankf, yrankf);
}

STAT_NAMESPACE_END

#endif /* STAT_CORRELATIONS_HEADER */
