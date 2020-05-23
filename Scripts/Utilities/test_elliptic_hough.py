# -*- coding: utf-8 -*-
"""
Created on Sat Jul 13 16:12:44 2019

@author: mvoulana
"""

import matplotlib.pyplot as plt

from skimage import data, color, img_as_ubyte
from skimage.feature import canny
from skimage.transform import hough_ellipse
from skimage.draw import ellipse_perimeter
from skimage.filters import sobel

import cv2
import numpy as np

from skimage.transform import hough_circle, hough_circle_peaks
from skimage.draw import circle_perimeter



def equalization(image):

    clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8,8))
    cl1 = clahe.apply(image)
    
    return cl1.astype(np.uint8)


# Load picture, convert to grayscale and detect edges
#image_rgb = data.coffee()[0:220, 160:420]
image_rgb = cv2.imread('../Images_test/test3.jpg')

print('1')
image_gray = color.rgb2gray(image_rgb)
#image_gray = cv2.cvtColor(image_rgb,cv2.COLOR_BGR2GRAY)

print('2')


"""----------------------- Canny edge detection ---------------------"""


edges = canny(image_gray, sigma=3.0, low_threshold=0.01, high_threshold=0.08)
print('3')

fig2, (ax1, ax2) = plt.subplots(ncols=2, nrows=1, figsize=(8, 4),
                                sharex=True, sharey=True)

ax1.set_title('Original picture')
ax1.imshow(image_gray)

ax2.set_title('Edge (white) and result (red)')
ax2.imshow(edges)

plt.show()


"""----------------------- Finding the contours ---------------------"""

"""
#--- First obtain the threshold using the greyscale image ---
ret,th = cv2.threshold(image_gray,140,255, 0)
plt.imshow(th)
plt.show()

#--- Find all the contours in the binary image ---
_, contours,hierarchy = cv2.findContours(th,2,1)
cnt = contours
big_contour = []
max = 0
for i in cnt:
   area = cv2.contourArea(i) #--- find the contour having biggest area ---
   if(area > max):
        max = area
        big_contour = i 

final = cv2.drawContours(image_rgb, big_contour, -1, (0,255,0), 3)
#cv2.imshow('final', final)
plt.imshow(final)
plt.show()
"""


"""----------------------- Circular Hough transform ---------------------"""

"""
# Detect two radii
hough_radii = np.arange(80, 150, 10)
hough_res = hough_circle(edges, hough_radii)

# Select the most prominent 3 circles
accums, cx, cy, radii = hough_circle_peaks(hough_res, hough_radii,
                                           total_num_peaks=1)

# Draw them
fig, ax = plt.subplots(ncols=1, nrows=1, figsize=(10, 4))
#image = color.gray2rgb(image)
for center_y, center_x, radius in zip(cy, cx, radii):
    circy, circx = circle_perimeter(center_y, center_x, radius)
    image_rgb[circy, circx] = (220, 20, 20)

ax.imshow(image_rgb, cmap=plt.cm.gray)
plt.show()
"""


"""----------------------- Elliptic Hough transform---------------------"""


# Perform a Hough Transform
# The accuracy corresponds to the bin size of a major axis.
# The value is chosen in order to get a single high accumulator.
# The threshold eliminates low accumulators

#result = hough_ellipse(edges)
#result = hough_ellipse(edges, threshold=50)
#result = hough_ellipse(edges, accuracy=256)
ret,th = cv2.threshold(image_gray,140,255, 0)
plt.imshow(th)
plt.show()


result = hough_ellipse(edges, min_size=100, max_size=120)
print('4')
#result.sort(order='accumulator')

"""
# Estimated parameters for the ellipse
best = list(result[-1])
yc, xc, a, b = [int(round(x)) for x in best[1:5]]
orientation = best[5]

# Draw the ellipse on the original image
cy, cx = ellipse_perimeter(yc, xc, a, b, orientation)
image_rgb[cy, cx] = (0, 0, 255)
# Draw the edge (white) and the resulting ellipse (red)
edges = color.gray2rgb(img_as_ubyte(edges))
edges[cy, cx] = (250, 0, 0)

fig2, (ax1, ax2) = plt.subplots(ncols=2, nrows=1, figsize=(8, 4),
                                sharex=True, sharey=True)

ax1.set_title('Original picture')
ax1.imshow(image_rgb)

ax2.set_title('Edge (white) and result (red)')
ax2.imshow(edges)

plt.show()
"""