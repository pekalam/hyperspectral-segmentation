from PyQt5.QtWidgets import QSlider, QLabel, QPushButton, QWidget

from gui.distanceMethodController import DistanceMethodController
from gui.hyperspectralImgModel import HyperspectralImgModel
from pcaDistanceSegmentation import pcaDistanceSegmentation


class PcaDistanceController(DistanceMethodController):
    def __init__(self, thrSlider: QSlider, thrVal: QLabel, applyBtn: QPushButton, panel: QWidget, maxComponentsSlider: QSlider, maxComponentsVal: QLabel, *args, **kwargs):
        self.onSegmentationFinished = None
        self.maxComponentsVal = maxComponentsVal
        self.maxComponentsSlider = maxComponentsSlider
        super().__init__(thrSlider, thrVal, applyBtn, panel, *args, **kwargs)
        maxComponentsSlider.valueChanged.connect(self.onMaxComponentsValChanged)

    def beginSegmentation(self):
        if self.img is not None and self.point is not None and self.orgSceneImg is not None:
            segmented = pcaDistanceSegmentation(self.point, self.img, self.orgSceneImg, self.slider.value(), self.maxComponentsSlider.value())
            self.onSegmentationFinished(segmented)

    def setOnSegmentationFinished(self, fn):
        self.onSegmentationFinished = fn

    def onMaxComponentsValChanged(self, val):
        self.maxComponentsVal.setText(str(val))
        self.applyBtn.setDisabled(False)

    def setImg(self, model: HyperspectralImgModel):
        DistanceMethodController.setImg(self, model)
        self.maxComponentsSlider.setMinimum(1)
        self.maxComponentsSlider.setMaximum(model.img.shape[2])
        self.maxComponentsSlider.setValue(model.img.shape[2] / 2)