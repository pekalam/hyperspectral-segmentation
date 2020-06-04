from PyQt5.QtGui import QImage
from spectral.io.bilfile import BilFile
import numpy as np


class HyperspectralImgModel:
    def __init__(self, img: BilFile, sceneImg: QImage, imgArr: np.ndarray = None):
        self.img: BilFile = img
        self.sceneImg: QImage = sceneImg
        if imgArr is None:
            self.imgArr = img.asarray().astype(np.float64).copy()
            # normalizacja min - max dla kazdego z bandów
            for i in range(0, self.imgArr.shape[2]):
                self.imgArr[:, :, i] = (self.imgArr[:, :, i] - self.imgArr[:, :, i].min()) / (
                            self.imgArr[:, :, i].max() - self.imgArr[:, :, i].min())
        else:
            self.imgArr = imgArr

