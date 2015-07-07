#!/usr/bin/env python

# -------------------------------------------------------------------
# Simple sum of squared differences (SSD) stereo-matching 
# -------------------------------------------------------------------

# The MIT License

# Copyright (c) 2015 David Christian

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
from PIL import Image


def stereo_match(left_img, right_img):
    # Load in both images. These are assumed to be RGBA 8bit per channel images
    left_img = Image.open(left_img)
    left = np.asarray(left_img)
    right_img = Image.open(right_img)
    right = np.asarray(right_img)

    # Initial squared differences
    w, h = left_img.size  # Assumes that both images are same size
    sd = np.empty((w, h), np.uint8)
    sd.shape = h, w

    # SSD support window (kernel)
    win_ssd = np.empty((w, h), np.uint16)
    win_ssd.shape = h, w
	
    # Depth (or disparity) map
    depth = np.empty((w, h), np.uint8)
    depth.shape = h, w

    # Minimum ssd difference between both images
    min_ssd = np.empty((w, h), np.uint16)
    min_ssd.shape = h, w
    for y in range(h):
        for x in range(w):
            min_ssd[y, x] = 65535  # Init to high value

    max_offset = 30
    offset_adjust = 255 / max_offset  # used to brighten depth map

    # Create ranges now instead of per loop
    y_range = range(h)
    x_range = range(w)
    x_range_ssd = range(w)

    # u and v support window
    window_range = range(-3, 3)

    # Main loop....
    for offset in range(max_offset):
        # Create initial image of squared differences between left and right image at the current offset
        for y in y_range:
            for x in x_range_ssd:
                if x - offset > 0:
                    diff = left[y, x, 0] - right[y, x - offset, 0]
                    sd[y, x] = diff * diff

		# Create a sum of squared differences over a support window at this offset
        for y in y_range:
            for x in x_range:
                sum_sd = 0
                for i in window_range:
                    for j in window_range:
                        # TODO: replace this expensive check by surrounding image with buffer / padding
                        if (-1 < y + i < h) and (-1 < x + j < w):
                            sum_sd += sd[y + i, x + j]

                # Store the sum in the window SSD image
                win_ssd[y, x] = sum_sd

        # Update the min ssd diff image with this new data
        for y in y_range:
            for x in x_range:
                # Is this new windowed SSD pixel a better match?
                if win_ssd[y, x] < min_ssd[y, x]:
                    # If so, store it and add to the depth map      
                    min_ssd[y, x] = win_ssd[y, x]
                    depth[y, x] = offset * offset_adjust

        print("Calculated offset ", offset)

    # Convert to PIL and save it
    Image.fromarray(depth).save('depth.png')


if __name__ == '__main__':
    #stereo_match("bowling_small_l.png", "bowling_small_r.png")
    stereo_match("view0.png", "view1.png")

