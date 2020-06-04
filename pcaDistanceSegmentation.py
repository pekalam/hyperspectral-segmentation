import cv2
import numpy as np
from PyQt5.QtCore import QPoint
from PyQt5.QtGui import QImage
from spectral.io.bilfile import BilFile
from distanceSegmentation import distanceSegmentation

def pcaDistanceSegmentation(p: QPoint, img: BilFile, orgSceneImg: QImage, threshold, maxComponents) -> QImage:
    imgarr = img.asarray()
    #zmiana rozmiaru macierzy na (dlugosc obrazu * szerokosc) x il. bandów
    imgarr = imgarr.reshape((imgarr.shape[0] * imgarr.shape[1], imgarr.shape[2]))
    #PCA
    mean, eigenv = np.array(cv2.PCACompute(imgarr, mean=None))
    #wybor n glownych skladowych i projekcja wsteczna
    reconstructed = cv2.PCABackProject(imgarr, mean[:, 0:maxComponents], eigenv[:, 0:maxComponents])
    #zmiana rozmiaru macierzy na pierwotny
    reconstructed = reconstructed.reshape(img.shape[0], img.shape[1], maxComponents)
    #metoda odleglosci dla nowej macierzy
    return distanceSegmentation(p, reconstructed, orgSceneImg, threshold)

