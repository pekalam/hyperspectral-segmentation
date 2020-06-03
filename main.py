from PyQt5.QtCore import QPoint

# read the image stack
# show the image

from PyQt5 import QtWidgets
from PyQt5 import uic
from PyQt5.QtGui import QImage
from PyQt5.QtWidgets import QLabel, QGraphicsView, QSlider, QPushButton, QWidget, QAction, QMenu
from spectral import *

from gui.distanceMethodController import DistanceMethodController
from gui.hyperspectralImgModel import HyperspectralImgModel
from gui.pcaDistanceController import PcaDistanceController
from gui.selectionPanelController import SelectionPanelController

class ImgSelectionController:
    IMG_FILES=['jasperRidge2_R198.hdr', 'samson_1.img.hdr', 'Urban_F210.hdr']

    def __init__(self, menu: QtWidgets.QMainWindow, *args, **kwargs):
        jasperRidge: QAction = menu.findChild(QAction, 'actionJasper_Ridge')
        samson: QAction = menu.findChild(QAction, 'actionSamson')
        urban: QAction = menu.findChild(QAction, 'actionUrban')

        self.onImgSelectedCallback = None
        self.selectedInd = 0
        jasperRidge.triggered.connect(self.onJasperEdgeSelected)
        urban.triggered.connect(self.onUrbanSelected)
        samson.triggered.connect(self.onSamsonSelected)

    def setOnImgSelected(self, fn):
        self.onImgSelectedCallback = fn

    def __raiseImgSelected(self):
        if self.onImgSelectedCallback is not None:
            self.onImgSelectedCallback(self.IMG_FILES[self.selectedInd])

    def onJasperEdgeSelected(self):
        self.selectedInd = 0
        self.__raiseImgSelected()

    def onUrbanSelected(self):
        self.selectedInd = 2
        self.__raiseImgSelected()

    def onSamsonSelected(self):
        self.selectedInd = 1
        self.__raiseImgSelected()




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

        self.imgSelectCtrl = ImgSelectionController(self)
        self.imgSelectCtrl.setOnImgSelected(self.onImgSelected)


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

    def onImgSelected(self, path: str):
        self.selPanelCtrl.loadImg(path)
        self.pcaSelPanelCtrl.loadImg(path)


app = QtWidgets.QApplication(sys.argv)
window = MainWindow()
window.show()
app.exec_()
