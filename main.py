from PyQt5.QtCore import QPoint

# read the image stack
# show the image

from PyQt5 import QtWidgets
from PyQt5 import uic
from PyQt5.QtGui import QImage
from PyQt5.QtWidgets import QLabel, QGraphicsView, QSlider, QPushButton, QWidget
from spectral import *

from gui.distanceMethodController import DistanceMethodController
from gui.hyperspectralImgModel import HyperspectralImgModel
from gui.pcaDistanceController import PcaDistanceController
from gui.selectionPanelController import SelectionPanelController


class MainWindow(QtWidgets.QMainWindow):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        uic.loadUi("mainwindowxx.ui", self)
        self.selPanelCtrl = SelectionPanelController(self.findChild(QGraphicsView, 'graphicsView'),
                                                     self.findChild(QLabel, 'label'),
                                                     self.findChild(QLabel, 'dstPixelPos'))
        self.distanceMethodController = DistanceMethodController(self.findChild(QSlider, 'dstThreshold'),
                                                                 self.findChild(QLabel, 'dstThresholdVal'),
                                                                 self.findChild(QPushButton, 'dstApplyBtn'),
                                                                 self.findChild(QWidget, 'dstMethodPanel'))
        self.selPanelCtrl.setOnImgClick(self.onImgClick)
        self.selPanelCtrl.setOnImgLoaded(self.onDstImgLoaded)
        self.distanceMethodController.setOnSegmentationFinished(self.onSegmentationFinished)

        self.pcaSelPanelCtrl = SelectionPanelController(self.findChild(QGraphicsView, 'pcaImg'),
                                                        self.findChild(QLabel, 'pcaResult')
                                                        , self.findChild(QLabel, 'pcaPixelPos'))
        self.pcaMethodController = PcaDistanceController(self.findChild(QSlider, 'pcaThreshold'),
                                                         self.findChild(QLabel, 'pcaThresholdVal'),
                                                         self.findChild(QPushButton, 'pcaApplyBtn'),
                                                         self.findChild(QWidget, 'pcaMethodPanel'),
                                                         self.findChild(QSlider, 'pcaMaxComponents'),
                                                         self.findChild(QLabel, 'pcaMaxComponentsVal'))
        self.pcaSelPanelCtrl.setOnImgClick(self.onPcaClick)
        self.pcaSelPanelCtrl.setOnImgLoaded(self.onPcaImgLoaded)
        self.pcaMethodController.setOnSegmentationFinished(self.onPcaSegmentationFinished)

        self.selPanelCtrl.loadImg('jasperRidge2_R198.hdr')
        self.pcaSelPanelCtrl.loadImg('jasperRidge2_R198.hdr')

    def onImgClick(self, imgPoint: QPoint):
        self.distanceMethodController.doSegmentationAt(imgPoint)

    def onPcaClick(self, imgPoint: QPoint):
        self.pcaMethodController.doSegmentationAt(imgPoint)

    def onPcaSegmentationFinished(self, img: QImage):
        self.pcaSelPanelCtrl.displayResult(img)

    def onSegmentationFinished(self, img: QImage):
        self.selPanelCtrl.displayResult(img)

    def onDstImgLoaded(self, model: HyperspectralImgModel):
        self.distanceMethodController.setImg(model)

    def onPcaImgLoaded(self, model: HyperspectralImgModel):
        self.pcaMethodController.setImg(model)


app = QtWidgets.QApplication(sys.argv)
window = MainWindow()
window.show()
app.exec_()
