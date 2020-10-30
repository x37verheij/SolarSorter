# Usage of various filters and enhancement actions.
# Practicum assignment 2.
# Meer info @ https://docs.opencv.org/3.1.0/d4/d13/tutorial_py_filtering.html
import cv2
import numpy as np
from matplotlib import pyplot as plt
from queue import Queue

# WINDOW_AUTOSIZE werkt niet, dus de getoonde afbeeldingen zullen verkleind (20%) worden weergegeven.
def show(name, image):
    im = cv2.resize(image, ((int) (2448 / 5 + 1), (int) (3264 / 5 + 1))) # Voor munten
    # im = cv2.resize(image, ((int) (2592 / 5 + 1), (int) (1944 / 5 + 1))) # Voor Bb bonen
    # im = cv2.resize(image, (400, 400)) # CUSTOM
    cv2.imshow(name, im) # Geeft hem weer als RGB
    # cv2.imshow(name, image)

# Plot twee plaatjes naast elkaar ter vergelijking van elkaar
def plot(name1, image1, name2, image2):
    plt.subplot(121),plt.imshow(image1),plt.title(name1)
    plt.xticks([]), plt.yticks([])
    plt.subplot(122),plt.imshow(image2),plt.title(name2)
    plt.xticks([]), plt.yticks([])
    plt.subplots_adjust(0.03, 0.03, 0.97, 0.97, 0.06, 0.06)
    plt.show()

# images = ['IMG_3643.JPG', 'IMG_3645.JPG', 'IMG_3646.JPG']
# images = ['IMG_3730.JPG', 'IMG_3731.JPG', 'IMG_3733.JPG', 'IMG_3732.JPG']
images = ['IMG_3737.JPG', 'IMG_3738.JPG']
# names = ['3643', '3645', '3646']
# names = ['3730', '3731', '3733', '3732']
names = ['3737', '3738']
# for img in images:
for i in range(0, 1):
    img = images[i]
    # Inlezen afbeelding met resolutie 3264 x 2448
    # img1 = cv2.imread('IMG_3646.JPG')
    # img1 = cv2.imread('IMG_3645.JPG')
    # img1 = cv2.imread('Untitled.png')
    # img1 = cv2.imread('50 cent.png')
    # img1 = cv2.imread('1 euro.png')
    img1 = cv2.imread(img) # Leest hem in als BGR
    # img1 = cv2.imread('pixels4.png')

    # img1 = cv2.imread('bb_image.bmp')
    # show('Origineel ' + img, img1)
    # img99 = cv2.imread('IMG_3644.JPG')
    # show('Origineel2', img99)
    # img1 = cv2.cvtColor(img1, cv2.COLOR_BGR2RGB)

    # GaussianBlur met een 9 x 9 kernel
    # img2 = cv2.GaussianBlur(img1,(9, 9), 0)
    # show ('Gauss 9 x 9', img2)
    # plot('Origineel', img1, 'Gauss 9 x 9', img2)

    # GaussianBlur met een 3 x 3 kernel
    # img3 = cv2.GaussianBlur(img1,(3, 3), 0)
    # show ('Gauss 3 x 3', img3)

    # Kleuren converteren
    img4 = cv2.cvtColor(img1, cv2.COLOR_BGR2GRAY)
    # show('gr ' + names[i], img4)
    # img5 = cv2.threshold(img4, 160, 255, cv2.THRESH_BINARY)[1]

    for j in range(0, 1):
        # img5 = cv2.threshold(img4, 100, 255, cv2.THRESH_BINARY)[1]
        img5 = cv2.threshold(img4, 160, 255, cv2.THRESH_BINARY)[1]
        # img5 = cv2.threshold(img4, 160 + j * 10, 255, cv2.THRESH_BINARY)[1]
        # img5b = cv2.threshold(img4, 170, 255, cv2.THRESH_BINARY)[1]
    # show('Grayscale', img4)
        # img5 = cv2.cvtColor(img5, cv2.COLOR_GRAY2BGR)
        # img5b = cv2.cvtColor(img5b, cv2.COLOR_GRAY2BGR)
        # show('BW ' + img + ' ' + str(160 + j * 5), img5)
        # cv2.imwrite('HD_' + names[i] + '.png', img5)
        # plot(
            # 'BW ' + img + ' 160', img5,
            # 'BW ' + img + ' 170', img5b)
    # print(cv2.countNonZero(img5))

    # img5 = cv2.cvtColor(img5, cv2.COLOR_BGR2GRAY)
    
    # Histogram in hsv
    imgh1 = cv2.cvtColor(img1, cv2.COLOR_BGR2HSV)
    # imgh1 = img1
    # show('HSV', imgh1)
    # imgh2 = cv2.cvtColor(imgh1, cv2.COLOR_HSV2BGR)
    # show('BGR', imgh2)
    # imgh3 = cv2.cvtColor(imgh1, cv2.COLOR_HSV2RGB)
    # show('RGB', imgh3)

    # color = ('b','g','r')
    # for j,col in enumerate(color):
        # plt.plot(cv2.calcHist([imgh1], [j], None, [256], [0, 256]), color = col)

    # h = cv2.calcHist([imgh1], [2], None, [256], [0, 256])
    # plt.plot(h)
    # plt.xlim([170, 220])
    # plt.show()
    # for h in imgh1[0]:
        # print(h, end=" ")

    # 2D Convolutie met acht keer -1 in een 3 x 3 kernel
    # kernel = np.ones((5, 5), np.float32) / 25
    # kernel = np.array([[1, -1, -1], [-1, 8, -1], [-1, -1, -1]]) / 1
    # img6 = cv2.filter2D(img1, -1, kernel)
    # img6 = cv2.cvtColor(img6, cv2.COLOR_GRAY2BGR)
    # img6 = cv2.cvtColor(img6, cv2.COLOR_RGB2BGR)

    # show('Convolutiefilter-1-1-1', img6)
    # plot('Origineel', img1, '2D Convolutiefilter', img6)

    for j in range(0, 1):
        # Erodes
        kernel = np.ones((3, 3), np.uint8)
        img7 = cv2.erode(img5, kernel, iterations = 10)

        # Dilates
        # kernel = np.ones((3, 3), np.uint8)
        # img7 = cv2.dilate(img5, kernel, iterations = 4)
        # img8 = cv2.dilate(img7, kernel, iterations = 90)
        img8 = cv2.dilate(img7, kernel, iterations = 20)
        # img8 = cv2.dilate(img7, kernel, iterations = 10 + j * 30)
        # img8b = cv2.dilate(img5, kernel, iterations = 85)
        # img7 = cv2.cvtColor(img7, cv2.COLOR_GRAY2RGB)
        # img8 = cv2.cvtColor(img8, cv2.COLOR_GRAY2RGB)
        # if j == 0: show('Eroded ' + str(10), img7)
        # show('Eroded ' + img, img7)
        # show('Dilated 5/90 ' + img, img8)
        # show('Dilated 0/85 ' + img, img8b)
        # show('Dilated ' + str(10 + j * 30), img8)
        # show('Eroded ' + str(4 * j), img7)
        # cv2.imwrite('image0001.png', img8)
        # plot(
            # 'Erode ' + img, img7,
            # 'Dilate ' + img, img8)

    # for a in range(0, 200):
    #     for b in range(0, 200):
    #         pass

    # Optellen bij Origineel
    # img1 = cv2.cvtColor(img1, cv2.COLOR_BGR2RGB)
    # img1 = cv2.cvtColor(img1, cv2.COLOR_RGB2BGR)
    # img8 = cv2.cvtColor(img8, cv2.COLOR_GRAY2RGB)
    # img9 = cv2.addWeighted(img8, 0.5, img1, 0.5, 0)
    # show('Added', img9)
    # show('Origineel ' + img, img1)

    print('beeldbewerkingen gedaan ' + img, flush = True)
    # img8 = img5 # without erodes & dilates

    # 
    # Groepen tellen
    # 
    # isFound array initialisatie
    isFound = np.zeros((len(img8), len(img8[0])), np.uint8)
    # print(img8)
    
    # Queue q initialisatie
    q = Queue()

    # Groups initialisatie
    groups = []

    # Loop over elke pixel
    for y in range(0, len(img8)):
        for x in range(0, len(img8[0])):
            if img8[y][x] == 0 and isFound[y][x] == 0:  # nog niet gevonden zwarte cel
                q.put((y, x))                         # voeg pixel toe aan de queue
                # print('>' + str(y) + ',' + str(x))
                groups.append(0)                      # creeer een nieuwe groep
                index = len(groups) - 1               # index wijst naar de nieuwe groep
                groups[index] = groups[index] + 1     # de groep is groter geworden
                isFound[y][x] = 1                     # deze pixel is nu gevonden
                while not q.empty():                  # zolang er connected pixels zijn gevonden
                    (yy, xx) = q.get()                # pak de volgende gevonden pixel
                    for yyy in range(yy - 1, yy + 2): # de pixels boven en onder
                        if yyy < 0: continue          # grensgeval yyy te klein
                        if yyy >= len(img8): continue # grensgeval yyy te groot
                        for xxx in range(xx - 1, xx + 2):           # de pixels links en rechts
                            if xxx < 0: continue                    # grensgeval xxx te klein
                            if xxx >= len(img8[0]): continue        # grensgeval xxx te groot
                            if isFound[yyy][xxx] == 0 and img8[yyy][xxx] == 0: # als de omliggende pixel nog niet gevonden is en zwart is
                                # print('<' + str(yyy) + ',' + str(xxx))
                                q.put((yyy, xxx))                   # voeg deze toe aan de queue
                                isFound[yyy][xxx] = 1               # en markeer deze als gevonden
                                groups[index] = groups[index] + 1   # de groep is groter geworden
            # print(str(y) + ',' + str(x) + '=' + str(img8[y][x]), flush = True)
        if y % 100 == 0: print(str(y) + ' / ' + str(len(img8)), flush = True)

    # De hele afbeelding is bekeken, dus nu weten we hoe groot de groepen zijn.
    realGroups = [] # groepen binnen de marges van 100000 en 20000
    for j in range(0, len(groups)):
        if groups[j] < 100000 and groups[j] > 20000:
            print(groups[j], end = ', ')
            realGroups.append(groups[j])
    print(img, 'has a total of', len(realGroups), 'groups', flush = True)

    # realGroups = []
    # if i == 0: realGroups = [53785, 63100, 41286, 63310, 53995, 47687, 41119, 42608, 69833, 58928, 79519, 50231, 46012]
    # else:      realGroups = [55223, 59987, 67232, 48140, 59678, 45870, 79943, 67475, 45009, 79688, 73820, 59490, 48736]

    # Percentages berekenen
    realPercentages = []
    maxPixels = 0
    leastPercentage = 100
    for j in range(0, len(realGroups)):
        if realGroups[j] > maxPixels: maxPixels = realGroups[j]
    
    for j in range(0, len(realGroups)):
        perc = realGroups[j] / maxPixels
        realPercentages.append(perc)
        if perc < leastPercentage: leastPercentage = perc
    
    # Vind aantal munten binnen range van leastPercentage (10 eurocent muntstuk)
    tiencentjes = 0
    for j in range(0, len(realPercentages)):
        if realPercentages[j] - leastPercentage < 0.07: tiencentjes = tiencentjes + 1
        # print(realPercentages[j], ',', leastPercentage, ',', realPercentages[j] - leastPercentage)

    print('Aantal gevonden 10 centjes in', names[i], 'is', tiencentjes)

cv2.waitKey(0)
