import cv2
import numpy as np
from PyQt5.QtCore import QPoint
from PyQt5.QtGui import QImage
from distanceSegmentation import distanceSegmentation
from gui.hyperspectralImgModel import HyperspectralImgModel


def pcaDistanceSegmentation(p: QPoint, model: HyperspectralImgModel, threshold, maxComponents) -> QImage:
    #zmiana rozmiaru macierzy na (dlugosc obrazu * szerokosc) x il. bandów
    imgarr = model.imgArr.reshape((model.imgArr.shape[0] * model.imgArr.shape[1], model.imgArr.shape[2]))
    #PCA
    mean, eigenv = np.array(cv2.PCACompute(imgarr, mean=None))
    #wybor n glownych skladowych i projekcja wsteczna
    reconstructed = cv2.PCABackProject(imgarr, mean[:, 0:maxComponents], eigenv[:, 0:maxComponents])
    #zmiana rozmiaru macierzy na pierwotny
    reconstructed = reconstructed.reshape(model.img.shape[0], model.img.shape[1], maxComponents)
    #metoda odleglosci dla nowej macierzy
    return distanceSegmentation(p, HyperspectralImgModel(model.img, model.sceneImg, reconstructed), threshold)

