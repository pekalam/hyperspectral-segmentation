from PyQt5.QtCore import QPoint

# read the image stack
# show the image

from PyQt5 import QtWidgets
from PyQt5 import uic
from PyQt5.QtGui import QImage
from PyQt5.QtWidgets import QLabel, QGraphicsView, QSlider
from spectral import *
from spectral.io.bilfile import BilFile
import cv2
import numpy as np

from distanceMethodController import DistanceMethodController
from distanceSegmentation import distanceSegmentation
from selectionPanelController import SelectionPanelController


def pcaDistanceSegmentation(p: QPoint, img: BilFile, orgSceneImg: QImage, threshold, maxComponents) -> QImage:
    imgarr = img.asarray()
    imgarr = imgarr.reshape((imgarr.shape[0] * imgarr.shape[1], imgarr.shape[2]))
    mean, eigenv = np.array(cv2.PCACompute(imgarr, mean=None))
    reconstructed = cv2.PCABackProject(imgarr, mean[:, 0:maxComponents], eigenv[:, 0:maxComponents])
    reconstructed = reconstructed.reshape(img.shape[0], img.shape[1], maxComponents)
    return distanceSegmentation(p, reconstructed, orgSceneImg, threshold)


class PcaDistanceController(DistanceMethodController):
    def __init__(self, thrSlider: QSlider, thrVal: QLabel, maxComponentsSlider: QSlider, maxComponentsVal: QLabel, *args, **kwargs):
        super().__init__(thrSlider, thrVal, *args, **kwargs)
        self.onSegmentationFinished = None
        self.maxComponentsVal = maxComponentsVal
        self.maxComponentsSlider = maxComponentsSlider
        maxComponentsSlider.valueChanged.connect(self.onMaxComponentsValChanged)
        maxComponentsSlider.setValue(50)

    def beginSegmentation(self):
        segmented = pcaDistanceSegmentation(self.point, self.img, self.orgSceneImg, self.slider.value(), self.maxComponentsSlider.value())
        self.onSegmentationFinished(segmented)

    def setOnSegmentationFinished(self, fn):
        self.onSegmentationFinished = fn

    def onMaxComponentsValChanged(self, val):
        self.maxComponentsVal.setText(str(val))
        if self.img is not None and self.point is not None and self.orgSceneImg is not None:
            self.beginSegmentation()


class MainWindow(QtWidgets.QMainWindow):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        uic.loadUi("mainwindowxx.ui", self)
        self.selPanelCtrl = SelectionPanelController(self.findChild(QGraphicsView, 'graphicsView'),
                                                     self.findChild(QLabel, 'label'),
                                                     self.findChild(QLabel, 'dstPixelPos'))
        self.selPanelCtrl.subscribeOnImgClick(self.onImgClick)

        self.distanceMethodController = DistanceMethodController(self.findChild(QSlider, 'dstThreshold'),
                                                                 self.findChild(QLabel, 'pcaThresholdVal'))
        self.distanceMethodController.subscribeOnSegmentationFinished(self.onSegmentationFinished)
        self.selPanelCtrl.loadImg('jasperRidge2_R198.hdr')

        self.pcaSelPanelCtrl = SelectionPanelController(self.findChild(QGraphicsView, 'pcaImg'),
                                                        self.findChild(QLabel, 'pcaResult')
                                                        , self.findChild(QLabel, 'pcaPixelPos'))
        self.pcaSelPanelCtrl.loadImg('jasperRidge2_R198.hdr')
        self.pcaSelPanelCtrl.subscribeOnImgClick(self.onPcaClick)

        self.pcaMethodController = PcaDistanceController(self.findChild(QSlider, 'pcaThreshold'),
                                                         self.findChild(QLabel, 'pcaThresholdVal'),
                                                         self.findChild(QSlider, 'pcaMaxComponents'),
                                                         self.findChild(QLabel, 'pcaMaxComponentsVal'))
        self.pcaMethodController.setOnSegmentationFinished(self.onPcaSegmentationFinished)

    def onImgClick(self, imgPoint: QPoint):
        self.distanceMethodController.startSegmentation(imgPoint, self.selPanelCtrl.file, self.selPanelCtrl.loadedImg)

    def onPcaClick(self, imgPoint: QPoint):
        self.pcaMethodController.startSegmentation(imgPoint, self.pcaSelPanelCtrl.file, self.pcaSelPanelCtrl.loadedImg)

    def onPcaSegmentationFinished(self, img: QImage):
        self.pcaSelPanelCtrl.displayResult(img)

    def onSegmentationFinished(self, img: QImage):
        self.selPanelCtrl.displayResult(img)


app = QtWidgets.QApplication(sys.argv)
window = MainWindow()
window.show()
app.exec_()
