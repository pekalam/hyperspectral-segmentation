from PyQt5.QtCore import QPoint, QCoreApplication
from PyQt5.QtGui import QImage
from PyQt5.QtWidgets import QSlider, QLabel, QPushButton, QWidget, QStatusBar

from distanceSegmentation import distanceSegmentation
from hyperspectralImgModel import HyperspectralImgModel


class DistanceMethodController:
    def __init__(self, thrSlider: QSlider, thrVal: QLabel, applyBtn: QPushButton, panel: QWidget, statusBar: QStatusBar, *args, **kwargs):
        self._slider: QSlider = thrSlider
        self._valLabel: QLabel = thrVal
        self._statusBar: QStatusBar = statusBar
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
        self._statusBar.showMessage("LOADING...")
        QCoreApplication.processEvents()
        self.beginSegmentation()
        self._statusBar.showMessage("")
        self._toggleControlsDisabled()

    def setImg(self, model: HyperspectralImgModel):
        self._model = model
        self._slider.setMinimum(0)
        self._slider.setMaximum(10 * 100)
        self._slider.setValue(1 * 100)
        self._applyBtn.setDisabled(True)
        self._firstSegmentation = False
        self._toggleControlsDisabled()

    def beginSegmentation(self):
        if self._firstSegmentation:
            segmented = distanceSegmentation(self._point, self._model, self._slider.value() / 100)
            self._raiseOnSegmentationFinished(segmented)

    def setOnSegmentationFinished(self, fn):
        self.__onSegmentationFinishedCallback = fn

    def onThresholdValueChanged(self, val):
        self._valLabel.setText(str(val / 100))
        self._applyBtn.setDisabled(False)

    def onApplyClicked(self):
        self._statusBar.showMessage("LOADING...")
        self._applyBtn.setDisabled(True)
        QCoreApplication.processEvents()
        self.beginSegmentation()
        self._statusBar.showMessage("")

    def _toggleControlsDisabled(self):
        self._panel.setDisabled(not self._firstSegmentation)

    def _raiseOnSegmentationFinished(self, img: QImage):
        if self.__onSegmentationFinishedCallback is not None:
            self.__onSegmentationFinishedCallback(img)