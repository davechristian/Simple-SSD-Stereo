Simple-SSD-Stereo
=================

This little script is for anyone interested in the basics of writing stereo-matching code. It's a simple implementation of a sum of squared differences (SSD), support-window based stereo-matching algorithm.

It takes a two photos, a left and right image of a subject taken from slightly different angles, and outputs a depth (disparity) map. Each pixel in the depth map indicates how far away it is from the camera - the darker it is, the further away it has been calculated to be, and vice versa.

Sample left:

![ScreenShot](https://raw.github.com/davechristian/Simple-SSD-Stereo/master/view0.png)

Sample right:

![ScreenShot](https://raw.github.com/davechristian/Simple-SSD-Stereo/master/view1.png)

Resulting depth map (with 6x6 pixel support window):

![ScreenShot](https://raw.github.com/davechristian/Simple-SSD-Stereo/master/depth.png)

It's not particularly fast (seriously.. you'll need to go make a cup of tea or something), but my aim was to experiment with the actual technique rather than make the fastest Python code in the world. I do intend to accelerate things using Numpy soon, however.

The bowling ball test images provided with this code are from the Middlebury stereo dataset 2006<sup>[1]</sup>.

The Python code depends on Numpy (http://www.numpy.org), and Pillow (https://github.com/python-pillow/Pillow), and is licensed under the MIT license (http://opensource.org/licenses/MIT). The current version of the code is written for Python 3.

References
----------
[1] H. Hirschmüller and D. Scharstein. Evaluation of cost functions for stereo matching.
In IEEE Computer Society Conference on Computer Vision and Pattern Recognition (CVPR 2007), Minneapolis, MN, June 2007
