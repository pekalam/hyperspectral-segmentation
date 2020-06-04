import numpy as np
from PyQt5.QtCore import QPoint, Qt
from PyQt5.QtGui import QImage, QColor, QPixmap


# oblicza odleglosc euklidesową od kazdego punktu obrazu do wybranego punktu na obrazie danego przez p
# zaznacza na obrazie orgSceneImg kolorem czerwonym punkty ktorych odleglosc byla mniejsza niz threshold
# arr - macierz obrazu hiperspektralnego o wymiarach np. 100x100x198
def distanceSegmentation(p: QPoint, arr: np.ndarray, orgSceneImg: QImage, threshold) -> QImage:
    matching = []
    # wybrany punkt na obrazie traktuje jako wektor ktorego elementami sa wartosci z poszczegolnych bandów
    vec1 = arr[p.y(), p.x(), :]
    imgCpy = orgSceneImg.copy()
    w = orgSceneImg.size().width()
    h = orgSceneImg.size().height()
    for i in range(0, arr.shape[1]):
        for j in range(0, arr.shape[0]):
            if i != p.x() or j != p.y():
                # dla reszty punktow na obrazie liczona jest odleglosc o pkt wybranego
                vec2 = arr[j, i, :]
                # liczenie odleglosci euklidesowej
                dif = np.subtract(vec2.astype(np.int32), vec1.astype(np.int32))
                dist = np.sqrt(np.sum(np.power(dif.astype(np.int64), 2)))
                # jezeli odleglosc jest mniejsza niz threshold dodaje punkt do tablicy
                if dist < threshold:
                    matching.append((i, j, dist))
    # zaznaczenie znalezionych punktow na obrazie
    for i in range(0, len(matching)):
        imgCpy.setPixelColor(matching[i][0], matching[i][1], QColor('red'))
    imgCpy.setPixelColor(p.x(), p.y(), QColor('red'))
    p = QPixmap.fromImage(imgCpy, Qt.AutoColor)
    return imgCpy
