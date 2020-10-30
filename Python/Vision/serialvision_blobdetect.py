import cv2 as cv
import numpy as np
from matplotlib import pyplot as plt
import random

random.seed(12345)

# Read image
image = cv.imread("CellPhoto001.jpg", cv.IMREAD_GRAYSCALE)

# Image dimensions
h = image.shape[0]
w = image.shape[1]
print(" h", h, " w", w)

# Crop points
y1 = int(h / 8 * 3)
y2 = int(h / 8 * 5)
# x1 = (w // 4) # not working with test image
# x2 = x1 * 3
x1 = int(w / 8 * 2)
x2 = int(w / 8 * 7)
print("y1", y1, "x1", x1)
print("y2", y2, "x2", x2)

# Grayscale (already done at imread)
# gray = cv.cvtColor(image, cv.COLOR_BGR2GRAY)

# Crop
crop = image[y1:y2, x1:x2]
# crop = gray[y1:y2, x1:x2]

# Binary threshold
# (thresh, im_bw) = cv.threshold(im, 128, 255, cv.THRESH_OTSU)
bw = cv.threshold(crop, 64, 255, cv.THRESH_BINARY)[1]

# bw = cv.adaptiveThreshold(crop,255,cv.ADAPTIVE_THRESH_MEAN_C,\
#             cv.THRESH_BINARY,11,2)

# Apply median filter to remove single speckles
bw = cv.medianBlur(bw, 3)

# Enlarge / zoom in 400%
bw = cv.resize(bw, ((int) (4 * (x2 - x1)), (int) (4 * (y2 - y1))))

# Detect bounding boxes
# ...
contours = cv.findContours(bw, cv.RETR_TREE, cv.CHAIN_APPROX_SIMPLE)[1]

# print(len(contours))

# https://docs.opencv.org/3.4/da/d0c/tutorial_bounding_rects_circles.html
# https://www.learnopencv.com/blob-detection-using-opencv-python-c/


# Set up the detector with default parameters.
# detector = cv.SimpleBlobDetector()

# Detect blobs.
# keypoints = detector.detect(image) # Doesn't work

# Draw detected blobs as red circles.
# cv.DRAW_MATCHES_FLAGS_DRAW_RICH_KEYPOINTS ensures the size of the\
# circle corresponds to the size of blob
# im_with_keypoints = cv.drawKeypoints(image, keypoints, np.array([]), 
#     (0,0,255), cv.DRAW_MATCHES_FLAGS_DRAW_RICH_KEYPOINTS)

# # Show keypoints
# cv.imshow("Keypoints", im_with_keypoints)

# Show image
cv.imshow("Gray", image)
# cv.imshow("Cropped", crop)
cv.imshow("BW", bw)
# cv.imshow("Edged", edged)
cv.waitKey(0)
