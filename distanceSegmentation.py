import numpy as np
from PyQt5.QtCore import QPoint, Qt
from PyQt5.QtGui import QImage, QColor, QPixmap
from hyperspectralImgModel import HyperspectralImgModel


# oblicza odleglosc euklidesową od kazdego punktu obrazu do wybranego punktu na obrazie danego przez p
# zaznacza na obrazie orgSceneImg kolorem czerwonym punkty ktorych odleglosc byla mniejsza niz threshold
# model zawiera znormalizowaną metodą min-max macierz obrazu hiperspektralnego o wymiarach np. 100x100x198
def distanceSegmentation(p: QPoint, model: HyperspectralImgModel, threshold) -> QImage:
    matching = []
    # wybrany punkt na obrazie traktuje jako wektor ktorego elementami sa wartosci z poszczegolnych bandów
    vec1 = model.imgArr[p.y(), p.x(), :]
    imgCpy = model.sceneImg.copy()
    w = imgCpy.size().width()
    h = imgCpy.size().height()
    for i in range(0, model.imgArr.shape[1]):
        for j in range(0, model.imgArr.shape[0]):
            if i != p.x() or j != p.y():
                # dla reszty punktow na obrazie liczona jest odleglosc o pkt wybranego
                vec2 = model.imgArr[j, i, :]
                # liczenie odleglosci euklidesowej
                dif = np.subtract(vec2, vec1)
                dist = np.sqrt(np.sum(np.power(dif, 2)))
                # jezeli odleglosc jest mniejsza niz threshold dodaje punkt do tablicy
                if dist < threshold:
                    matching.append((i, j, dist))
    # zaznaczenie znalezionych punktow na obrazie
    for i in range(0, len(matching)):
        imgCpy.setPixelColor(matching[i][0], matching[i][1], QColor('red'))
    imgCpy.setPixelColor(p.x(), p.y(), QColor('red'))
    p = QPixmap.fromImage(imgCpy, Qt.AutoColor)
    return imgCpy
