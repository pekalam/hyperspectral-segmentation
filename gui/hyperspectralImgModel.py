from PyQt5.QtGui import QImage
from spectral.io.bilfile import BilFile


class HyperspectralImgModel:
    def __init__(self, img: BilFile, sceneImg: QImage):
        self.img: BilFile = img
        self.sceneImg: QImage = sceneImg