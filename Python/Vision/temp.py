import cv2
import numpy as np

kernel = np.ones((5, 5), np.uint8)
img = cv2.imread("im1.bmp")

# cuts holds the original photos of the cells
cuts = [0]*12
cuts[0] = img[165:279, :201]
cuts[1] = img[165:279, 201:404]
cuts[2] = img[165:279, 404:603]
cuts[3] = img[165:279, 603:]
cuts[4] = img[279:383, :201]
cuts[5] = img[279:383, 201:404]
cuts[6] = img[279:383, 404:603]
cuts[7] = img[279:383, 603:]
cuts[8] = img[383:497, :201]
cuts[9] = img[383:497, 201:404]
cuts[10] = img[383:497, 404:603]
cuts[11] = img[383:497, 603:]

for i in range(len(cuts)):
    org = cuts[i]
    img = cv2.cvtColor(org, cv2.COLOR_BGR2GRAY)                         # Grayscale
    img = cv2.threshold(img, 64, 255, cv2.THRESH_BINARY)[1]             # BW
    img = cv2.morphologyEx(img, cv2.MORPH_OPEN, kernel, iterations=2)   # Close holes
    if cv2.countNonZero(img) < 15000:
        cv2.imwrite("Cut\\" + str(i + 1) + ".png", org)

    # cv2.imshow(str(id), img)
    # cv2.imwrite(name, cuts[i])
    



# gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
# bw = cv2.threshold(gray, 127, 255, cv2.THRESH_BINARY)[1]

# Setup SimpleBlobDetector parameters.
# params = cv2.SimpleBlobDetector_Params()
# params.minThreshold = 0
# params.maxThreshold = 64
# params.blobColor = 0
# params.filterByArea = True
# params.minArea = 10000  # generally 19k+
# detector = cv2.SimpleBlobDetector_create(params)

# kernel = np.ones((3, 3), np.uint8)
# blobs = cv2.erode(bw, kernel, iterations = 10)
# print("hi")
# detector = cv2.SimpleBlobDetector()
# print("hi")
# keypoints = detector.detect(img)
# print(keypoints, flush=True)
# Draw red outlines
# im_with_keypoints = cv2.drawKeypoints(img, keypoints, np.array([]), (0,0,255), cv2.DRAW_MATCHES_FLAGS_DRAW_RICH_KEYPOINTS)



# cv2.imshow("Original", img)
# cv2.imshow("Grayscale", gray)
# cv2.imshow("Black & white", bw)
# cv2.imshow("Blobs", blobs)
# cv2.imwrite('cellindex.png', bw)
# cv2.imshow("Keypoints", im_with_keypoints)
# cv2.imshow("BW 63", bw1)
# cv2.imshow("BW 127", bw2)
# cv2.imshow("BW 191", bw3)
cv2.waitKey()
