import cv2
import numpy as np
import matplotlib.pyplot as plt
import math
from util import openFile, showImage
from holdDetector import buildDetector


imgOrig = grab_from_file()
gray = cv2.cvtColor(imgOrig,cv2.COLOR_BGR2GRAY)
detector = buildDetector()

th = 50
def draw(img, keypoints):
    # Draw detected blobs as red circles.
    # cv2.DRAW_MATCHES_FLAGS_DRAW_RICH_KEYPOINTS ensures the 
    # size of the circle corresponds to the size of blob
    for i, key in enumerate(keypoints):
        x = int(key.pt[0])
        y = int(key.pt[1])

        size = int(math.ceil(key.size)) 

        #Finds a rectangular window in which the keypoint fits
        br = (x + size, y + size)   
        tl = (x - size, y - size)
        cv2.rectangle(img,tl,br,(0,0,255),2)

    #OpenCV uses BGR format, so that'll need to be reversed for display
    img = img[...,::-1]


while 1:
    img = imgOrig.copy()

    edges = cv2.Canny(img,th, th * 1.2, L2gradient = True)

    contours, _ = cv2.findContours(edges,cv2.RETR_LIST,cv2.CHAIN_APPROX_SIMPLE)

    # Applies convex hulls to each contour, ensuring each contour
    # is a closed polygon.
    hulls = map(cv2.convexHull,contours)

    # Draws contours onto a blank canvas
    mask = np.zeros(img.shape,np.uint8)
    cv2.drawContours(mask,contours,-1,[255,255,255],-1)

    if detector == None:
        # Set up the detector with default parameters.
        detector = buildDetector()

    keypoints = detector.detect(mask)





    print th

    draw(img,keypoints)
    cv2.imshow('Fig',img)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
    elif cv2.waitKey(1) & 0xFF == ord('p'):
        th= th + 10
    elif cv2.waitKey(1) & 0xFF == ord('m'):
        th= th - 10



