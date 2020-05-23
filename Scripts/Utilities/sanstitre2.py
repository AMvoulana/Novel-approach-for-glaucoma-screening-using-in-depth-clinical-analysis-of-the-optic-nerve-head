# -*- coding: utf-8 -*-
"""
Created on Sat Jul 13 18:10:57 2019

@author: mvoulana
"""

from skimage.transform import hough_ellipse
from skimage.draw import ellipse_perimeter
import matplotlib.pyplot as plt


img = np.zeros((25, 25), dtype=np.uint8)
rr, cc = ellipse_perimeter(10, 10, 6, 8)
img[cc, rr] = 1

plt.imshow(img)
plt.show()

result = hough_ellipse(img, threshold=8)
result.tolist()