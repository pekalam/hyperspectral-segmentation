from PyQt5.QtWidgets import QSlider, QLabel, QPushButton, QWidget, QStatusBar

from gui.distanceMethodController import DistanceMethodController
from gui.hyperspectralImgModel import HyperspectralImgModel
from pcaDistanceSegmentation import pcaDistanceSegmentation


class PcaDistanceController(DistanceMethodController):
    def __init__(self, thrSlider: QSlider, thrVal: QLabel, applyBtn: QPushButton, panel: QWidget, statusBar: QStatusBar,
                 maxComponentsSlider: QSlider, maxComponentsVal: QLabel, *args, **kwargs):
        self._maxComponentsVal = maxComponentsVal
        self._maxComponentsSlider = maxComponentsSlider
        super().__init__(thrSlider, thrVal, applyBtn, panel, statusBar, *args, **kwargs)
        maxComponentsSlider.valueChanged.connect(self.onMaxComponentsValChanged)

    def beginSegmentation(self):
        if self._firstSegmentation:
            segmented = pcaDistanceSegmentation(self._point, self._model, self._slider.value() / 100,
                                                self._maxComponentsSlider.value())
            self._raiseOnSegmentationFinished(segmented)

    def onMaxComponentsValChanged(self, val):
        self._maxComponentsVal.setText(str(val))
        self._applyBtn.setDisabled(False)

    def setImg(self, model: HyperspectralImgModel):
        DistanceMethodController.setImg(self, model)
        self._maxComponentsSlider.setMinimum(1)
        self._maxComponentsSlider.setMaximum(model.img.shape[2])
        self._maxComponentsSlider.setValue(model.img.shape[2] / 2)
