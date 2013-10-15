#!/usr/bin/env python

# -------------------------------------------------------
# Simple sum of squared differences (SSD) stereo-matching 
# -------------------------------------------------------

# The MIT License

# Copyright (c) 2013 David Christian

# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:

# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.

# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
# THE SOFTWARE.

import numpy as np
import matplotlib.pyplot as plt
import PIL


def stereo_match(left_img, right_img):
    # Load in both images. These are assumed to be RGBA format images
    left_img = PIL.Image.open(left_img)
    left = np.asarray(left_img)
    right_img = PIL.Image.open(right_img)
    right = np.asarray(right_img)

    # Initial SSD
    w, h = left_img.size  # Assumes that both images are same size
    ssd = np.empty((w, h), np.uint8)
    ssd.shape = h, w

    # SSD support window (kernel)
    win_ssd = np.empty((w, h), np.uint16)
    win_ssd.shape = h, w

    # Depth (or disparity) map
    depth = np.empty((w, h), np.uint8)
    depth.shape = h, w

    # Minimum ssd difference between both images
    min_ssd = np.empty((w, h), np.uint16)
    min_ssd.shape = h, w
    for y in xrange(h):
        for x in xrange(w):
            min_ssd[y, x] = 65535  # Init to high value

    max_offset = 30
    offset_adjust = 255 / max_offset  # used to brighten depth map

    # Create ranges now instead of per loop
    y_range = xrange(h)
    x_range = xrange(w)
    x_range_ssd = xrange(w)

    # u and v support window (currently -4 to 4, so 8x8)
    window_range = xrange(-4, 5)

    # Main loop....
    for offset in xrange(max_offset):
    # Create initial image of squared differences between left and right image at the current offset
        for y in y_range:
            for x in x_range_ssd:
                if x - offset > 0:
                    diff = left[y, x, 0] - right[y, x - offset, 0]
                    ssd[y, x] = diff * diff

        # Create a sum of squared differences over a support window at this offset
        for y in y_range:
            for x in x_range:
                sum_sad = 0
                for i in window_range:
                    for j in window_range:
                        # TODO: I need to replace this expensive check by surrounding image with buffer
                        if (-1 < y + i < h) and (-1 < x + j < w):
                            sum_sad += ssd[y + i, x + j]

                # Store the sum in the window SSD image
                win_ssd[y, x] = sum_sad

        # Update the min ssd diff image with this new data
        for y in y_range:
            for x in x_range:
                # Is this new windowed SSD pixel a better match?
                if win_ssd[y, x] < min_ssd[y, x]:
                    # If so, store it and add to the depth map      
                    min_ssd[y, x] = win_ssd[y, x]
                    depth[y, x] = offset * offset_adjust

        print "Calculated offset ", offset

    # Convert to PIL and save it
    PIL.Image.fromarray(depth).save('depth.png')


if __name__ == '__main__':
    stereo_match("bowling_small_l.png", "bowling_small_r.png")

