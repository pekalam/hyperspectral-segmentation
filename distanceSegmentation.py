import numpy as np
from PyQt5.QtCore import QPoint, Qt
from PyQt5.QtGui import QImage, QColor, QPixmap

def distanceSegmentation(p: QPoint, arr: np.ndarray, orgSceneImg: QImage, threshold) -> QImage:
    matching = []
    vec1 = arr[p.y(), p.x(), :]
    imgCpy = orgSceneImg.copy()
    w = orgSceneImg.size().width()
    h = orgSceneImg.size().height()
    for i in range(0, arr.shape[1]):
        for j in range(0, arr.shape[0]):
            if i != p.x() or j != p.y():
                vec2 = arr[j, i, :]
                dif = np.subtract(vec2, vec1).astype(np.int32)
                dist = np.sum(np.sqrt(np.power(dif, 2).astype(np.int64)))
                if dist < threshold:
                    matching.append((i, j, dist))
    for i in range(0, len(matching)):
        imgCpy.setPixelColor(matching[i][0], matching[i][1], QColor('red'))
    imgCpy.setPixelColor(p.x(), p.y(), QColor('red'))
    p = QPixmap.fromImage(imgCpy, Qt.AutoColor)
    return imgCpy