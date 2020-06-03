import numpy as np
from PyQt5.QtCore import QPoint, Qt
from PyQt5.QtGui import QImage, QColor, QPixmap
from spectral.io.bilfile import BilFile


def distanceSegmentation(p: QPoint, arr: np.ndarray, orgSceneImg: QImage, threshold) -> QImage:
    matching = []
    vec1 = arr[p.y(), p.x(), :]
    imgCpy = orgSceneImg.copy()
    for i in range(0, orgSceneImg.size().width()):
        for j in range(0, orgSceneImg.size().height()):
            if i != p.x() or j != p.y():
                vec2 = arr[j, i, :]
                dif = np.subtract(vec2, vec1).astype(np.int32)
                dist = np.sum(np.sqrt(np.power(dif, 2).astype(np.int64)))
                if dist < threshold:
                    matching.append((i, j, dist))
    for i in range(0, len(matching)):
        imgCpy.setPixelColor(matching[i][0], matching[i][1], QColor('white'))
    imgCpy.setPixelColor(p.x(), p.y(), QColor('white'))
    p = QPixmap.fromImage(imgCpy, Qt.AutoColor)
    return imgCpy