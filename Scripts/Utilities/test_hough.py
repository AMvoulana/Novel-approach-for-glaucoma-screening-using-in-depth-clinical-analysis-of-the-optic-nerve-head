# -*- coding: utf-8 -*-
"""
Created on Sat Jul 13 16:00:51 2019

@author: mvoulana
"""

import cv2
import numpy as np
import matplotlib.pyplot as plt


img = cv2.imread('../Images_test/test1.jpg',0)
#img = cv2.medianBlur(img,5)

cimg = cv2.cvtColor(img,cv2.COLOR_GRAY2BGR)


circles = cv2.HoughCircles(img,cv2.HOUGH_GRADIENT,1,60,
                            param1=40,param2=30,minRadius=60,maxRadius=0)

circles = np.uint16(np.around(circles))
for i in circles[0,:]:
    # draw the outer circle
    cv2.circle(cimg,(i[0],i[1]),i[2],(0,255,0),2)
    # draw the center of the circle
    cv2.circle(cimg,(i[0],i[1]),2,(0,0,255),3)

plt.imshow(cimg)
plt.show()

"""
cv2.imshow('detected circles',cimg)
cv2.waitKey(0)
cv2.destroyAllWindows()
"""