from PyQt5.QtCore import QPoint
from PyQt5.QtGui import QImage
from PyQt5.QtWidgets import QSlider, QLabel, QPushButton, QWidget
from spectral.io.bilfile import BilFile

from distanceSegmentation import distanceSegmentation
from gui.hyperspectralImgModel import HyperspectralImgModel


class DistanceMethodController:
    def __init__(self, thrSlider: QSlider, thrVal: QLabel, applyBtn: QPushButton, panel: QWidget, *args, **kwargs):
        self._slider: QSlider = thrSlider
        self._valLabel: QLabel = thrVal
        self._applyBtn = applyBtn
        self._panel = panel
        self._point = None
        self._firstSegmentation = False
        self._model: HyperspectralImgModel = None
        self.__onSegmentationFinishedCallback = None
        applyBtn.clicked.connect(self.onApplyClicked)
        thrSlider.valueChanged.connect(self.onThresholdValueChanged)
        self._toggleControlsDisabled()

    def doSegmentationAt(self, p: QPoint):
        self._point = p
        self._firstSegmentation = True
        self.beginSegmentation()
        self._toggleControlsDisabled()

    def setImg(self, model: HyperspectralImgModel):
        self._model = model
        self._slider.setMinimum(0)
        self._slider.setMaximum(50_000)
        self._slider.setValue(30_000)
        self._applyBtn.setDisabled(True)

    def beginSegmentation(self):
        if self._firstSegmentation:
            segmented = distanceSegmentation(self._point, self._model.img.asarray(), self._model.sceneImg, self._slider.value())
            self._raiseOnSegmentationFinished(segmented)

    def setOnSegmentationFinished(self, fn):
        self.__onSegmentationFinishedCallback = fn

    def onThresholdValueChanged(self, val):
        self._valLabel.setText(str(val))
        self._applyBtn.setDisabled(False)

    def onApplyClicked(self):
        self.beginSegmentation()
        self._applyBtn.setDisabled(True)

    def _toggleControlsDisabled(self):
        self._panel.setDisabled(not self._firstSegmentation)

    def _raiseOnSegmentationFinished(self, img: QImage):
        if self.__onSegmentationFinishedCallback is not None:
            self.__onSegmentationFinishedCallback(img)