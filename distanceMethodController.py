from PyQt5.QtCore import QPoint
from PyQt5.QtGui import QImage
from PyQt5.QtWidgets import QSlider, QLabel
from spectral.io.bilfile import BilFile

from distanceSegmentation import distanceSegmentation


class DistanceMethodController:
    def __init__(self, thrSlider: QSlider, thrVal: QLabel, *args, **kwargs):
        self.slider: QSlider = thrSlider
        self.valLabel: QLabel = thrVal
        self.onSegmentationFinishedCallbacks = []
        self.img = None
        self.point = None
        self.orgSceneImg = None
        thrSlider.valueChanged.connect(self.onThresholdValueChanged)
        thrSlider.setMinimum(0)
        thrSlider.setMaximum(50_000)
        thrSlider.setValue(30_000)

    def startSegmentation(self, p: QPoint, img: BilFile, orgSceneImg: QImage):
        self.img: BilFile = img
        self.point = p
        self.orgSceneImg = orgSceneImg
        self.beginSegmentation()

    def setImg(self, img: BilFile, orgSceneImg: QImage):
        self.img: BilFile = img
        self.orgSceneImg = orgSceneImg

    def beginSegmentation(self):
        segmented = distanceSegmentation(self.point, self.img.asarray(), self.orgSceneImg, self.slider.value())
        self.__raiseOnSegmentationFinished(segmented)

    def __raiseOnSegmentationFinished(self, img: QImage):
        for f in self.onSegmentationFinishedCallbacks:
            f(img)

    def subscribeOnSegmentationFinished(self, fn):
        self.onSegmentationFinishedCallbacks.append(fn)

    def onThresholdValueChanged(self, val):
        self.valLabel.setText(str(val))
        if self.img is not None and self.point is not None and self.orgSceneImg is not None:
            self.beginSegmentation()
