

# from ftplib import FTP
# ftp = FTP(host="192.168.0.11", user="admin", timeout=3)

# with open('image.jpg', 'wb') as imageBuffer:
#     ftp.retrbinary('RETR image.jpg', imageBuffer.write)
#     imageBuffer.close()

# ftp.quit()

import cv2
img = cv2.imread("cellindex_numbered.png")

# Isolate all cell locations
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

for i in range(12):
    name = str(i + 1) + ".png"
    # cv2.imwrite(name, cuts[i])

cv2.waitKey()
