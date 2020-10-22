import cv2
import numpy as np

# def nothing():
#     pass
#     """
# from ftplib import FTP
# ftp = FTP(host="192.168.0.11", user="admin", timeout=3)

# with open('image.jpg', 'wb') as imageBuffer:
#     ftp.retrbinary('RETR image.jpg', imageBuffer.write)
#     imageBuffer.close()

# ftp.quit()

img = cv2.imread("image.jpg")

# Bijsnijden/crop. vanaf y = 150 tot y = 500
crop = img[150:500, 0:800]


gray = cv2.cvtColor(crop, cv2.COLOR_BGR2GRAY)
bw = cv2.threshold(gray, 64, 255, cv2.THRESH_BINARY)[1]

# Setup SimpleBlobDetector parameters.
params = cv2.SimpleBlobDetector_Params()
# params.minThreshold = 0
# params.maxThreshold = 64
params.blobColor = 0
params.filterByArea = True
params.minArea = 10000  # generally 19k+
detector = cv2.SimpleBlobDetector_create(params)

kernel = np.ones((3, 3), np.uint8)
blobs = cv2.erode(bw, kernel, iterations = 10)
# print("hi")
# detector = cv2.SimpleBlobDetector()
print("hi")
keypoints = detector.detect(crop)
print(keypoints, flush=True)
# Draw red outlines
im_with_keypoints = cv2.drawKeypoints(crop, keypoints, np.array([]), (0,0,255), cv2.DRAW_MATCHES_FLAGS_DRAW_RICH_KEYPOINTS)



# cv2.imshow("Original", crop)
# cv2.imshow("Grayscale", gray)
# cv2.imshow("Black & white", bw)
# cv2.imshow("Blobs", blobs)
# cv2.imwrite('blobs.png', blobs)
# cv2.imshow("Keypoints", im_with_keypoints)
# cv2.imshow("BW 63", bw1)
# cv2.imshow("BW 127", bw2)
# cv2.imshow("BW 191", bw3)
cv2.waitKey()
# """