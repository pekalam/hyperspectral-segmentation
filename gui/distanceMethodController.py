from PyQt5.QtCore import QPoint
from PyQt5.QtGui import QImage
from PyQt5.QtWidgets import QSlider, QLabel, QPushButton, QWidget
from spectral.io.bilfile import BilFile

from distanceSegmentation import distanceSegmentation
from gui.hyperspectralImgModel import HyperspectralImgModel


class DistanceMethodController:
    def __init__(self, thrSlider: QSlider, thrVal: QLabel, applyBtn: QPushButton, panel: QWidget, *args, **kwargs):
        self.slider: QSlider = thrSlider
        self.valLabel: QLabel = thrVal
        self.applyBtn = applyBtn
        self.panel = panel
        self.onSegmentationFinishedCallback = None
        self.img = None
        self.point = None
        self.orgSceneImg = None
        applyBtn.clicked.connect(self.onApplyClicked)
        thrSlider.valueChanged.connect(self.onThresholdValueChanged)
        self._toggleControlsDisabled()

    def startSegmentation(self, p: QPoint, img: BilFile, orgSceneImg: QImage):
        self.img: BilFile = img
        self.point = p
        self.orgSceneImg = orgSceneImg
        self.beginSegmentation()
        self._toggleControlsDisabled()

    def setImg(self, model: HyperspectralImgModel):
        self.slider.setMinimum(0)
        self.slider.setMaximum(50_000)
        self.slider.setValue(30_000)

    def beginSegmentation(self):
        if self._isSegementationDone():
            segmented = distanceSegmentation(self.point, self.img.asarray(), self.orgSceneImg, self.slider.value())
            self.__raiseOnSegmentationFinished(segmented)

    def setOnSegmentationFinished(self, fn):
        self.onSegmentationFinishedCallback = fn

    def onThresholdValueChanged(self, val):
        self.valLabel.setText(str(val))
        self.applyBtn.setDisabled(False)

    def onApplyClicked(self):
        self.beginSegmentation()
        self.applyBtn.setDisabled(True)

    def _isSegementationDone(self) -> bool:
        return self.img is not None and self.point is not None and self.orgSceneImg is not None

    def _toggleControlsDisabled(self):
        segDone = self._isSegementationDone()
        self.panel.setDisabled(not segDone)

    def __raiseOnSegmentationFinished(self, img: QImage):
        if self.onSegmentationFinishedCallback is not None:
            self.onSegmentationFinishedCallback(img)