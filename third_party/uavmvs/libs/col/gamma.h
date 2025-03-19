/*
 * Copyright (C) 2016-2018, Nils Moehrle
 * All rights reserved.
 *
 * This software may be modified and distributed under the terms
 * of the BSD 3-Clause license. See the LICENSE.txt file for details.
 */

#ifndef COL_GAMMA_HEADER
#define COL_GAMMA_HEADER

#include <type_traits>

#include "defines.h"

COL_NAMESPACE_BEGIN

template <typename T>
void gamma_encode_srgb(T * color) {
    static_assert(std::is_floating_point<T>::value,
        "Floating point type required");
    for (int i = 0; i < 3; ++i) {
        if (color[i] <= T(0.0031308)) {
            color[i] *= T(12.92);
        } else {
            T tmp = std::pow(color[i], T(1.0) / T(2.4));
            color[i] = T(1.055) * tmp - T(0.055);
        }
    }
}

template <typename T>
void gamma_decode_srgb(T * color) {
    static_assert(std::is_floating_point<T>::value,
        "Floating point type required");
    for (int i = 0; i < 3; ++i) {
        if (color[i] <= T(0.04054)) {
            color[i] /= T(12.92);
        } else {
            T base = (color[i] + T(0.055)) / T(1.055);
            color[i] = std::pow(base, T(2.4));
        }
    }
}

COL_NAMESPACE_END

#endif /* COL_GAMMA_HEADER */
