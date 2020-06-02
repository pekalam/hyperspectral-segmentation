from PyQt5.QtCore import Qt, QPoint
from skimage import io
import numpy as np
import matplotlib.pyplot as plt

# read the image stack
# show the image

from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5 import uic
from PyQt5.QtGui import QPixmap, QImage, QColor, QPainterPath, QPen
from PyQt5.QtWidgets import QLabel, QSlider, QGraphicsView, QGraphicsScene, QGraphicsPixmapItem
from spectral import *
from spectral.graphics import get_rgb
import math

class MainWindow(QtWidgets.QMainWindow):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        uic.loadUi("mainwindowxx.ui", self)
        #self.a: QLabel = self.findChild(QLabel, 'label')
        self.a: QGraphicsView = self.findChild(QGraphicsView, 'graphicsView')
        self.a.setScene(QGraphicsScene())
        self.a.setViewportUpdateMode(QGraphicsView.FullViewportUpdate)
        self.resultLabel: QLabel = self.findChild(QLabel, 'label')
        #slider: QSlider = self.findChild(QSlider, 'slider')
        #slider.setMaximum(100)
        #slider.setMinimum(1)
        #slider.valueChanged.connect(self.sliderValChanged)
        self.a.mousePressEvent = self.onImgClick
        self.loadImg()
        self.renderCross(QPoint(200,200))

    def onImgClick(self, event):
        point = event.pos()
        item = self.a.itemAt(point)
        scenePoint = self.a.mapToScene(point)
        if item is None:
            return
        mapped = item.mapFromScene(scenePoint)
        imgPoint = QPoint(mapped.x() / 8, mapped.y()/8)
        self.updateCross(scenePoint)
        self.findSegments(imgPoint)

    def sliderValChanged(self, val):
        self.scaleImg(val)

    def loadImg(self):
        self.imgs = open_image('jasperRidge2_R198.hdr')
        self.arr = self.imgs.asarray()
        rgb = get_rgb(self.imgs)
        rgb = rgb * 255
        rgb = rgb.astype(np.uint8)
        self.i = QImage(rgb.tobytes(), rgb.shape[0], rgb.shape[1], rgb.shape[0] * 3, QImage.Format_RGB888)

        p = QPixmap.fromImage(self.i, Qt.AutoColor)
        self.imgItem: QGraphicsPixmapItem = self.a.scene().addPixmap(p)
        self.scaleImg(8)
        #self.a.setPixmap(p)
        #self.a.setMask(p.mask())

    def findSegments(self, p: QPoint):
        matching = []
        vec1 = self.arr[p.y(), p.x(), :]
        imgCpy = self.i.copy()
        for ii in range(0, self.i.size().width()):
            for jj in range(0, self.i.size().height()):
                if ii != p.x() or jj != p.y():
                    vec2 = self.arr[jj, ii, :]
                    dif = np.subtract(vec2, vec1).astype(np.int32)
                    dist = np.sum(np.sqrt(np.power(dif, 2).astype(np.int64)))
                    if dist < 30_000:
                        matching.append((ii,jj,dist))
        for i in range(0, len(matching)):
            imgCpy.setPixelColor(matching[i][0],matching[i][1], QColor('white'))
        imgCpy.setPixelColor(p.x(), p.y(), QColor('white'))
        p = QPixmap.fromImage(imgCpy, Qt.AutoColor)
        self.resultImg = imgCpy
        self.resultLabel.setPixmap(p)
        self.resultLabel.setMask(p.mask())
        self.scaleResult()

    def scaleImg(self, factor):
        p = QPixmap.fromImage(self.i.scaled(self.i.size().width() * factor, self.i.size().height() * factor),
                              Qt.AutoColor)

        self.a.scene().removeItem(self.imgItem)
        self.imgItem: QGraphicsPixmapItem = self.a.scene().addPixmap(p)

        #self.a.setPixmap(p)
        #self.a.setMask(p.mask())

    def scaleResult(self):
        destW = self.imgItem.pixmap().width() if self.resultLabel.size().width() > self.imgItem.pixmap().width() \
            else self.resultLabel.size().width()
        destH = self.imgItem.pixmap().height() if self.resultLabel.size().height() > self.imgItem.pixmap().height() \
            else self.resultLabel.size().height()
        sw = destW
        sh = destH

        if self.resultImg.width() * sh > sw * self.resultImg.height():
            destH = sw * self.resultImg.height() / self.resultImg.width()
        else:
            destW = sh * self.resultImg.width() / self.resultImg.height()
        p = QPixmap.fromImage(self.resultImg.scaled(destW, destH))
        self.resultLabel.setPixmap(p)
        self.resultLabel.setMask(p.mask())

    def renderCross(self, p: QPoint):
        path = QPainterPath()
        path.moveTo(10, 0)
        path.lineTo(10,  + 20)
        path.moveTo(0, 10)
        path.lineTo(20, 10)

        pen = QPen(QColor(255,0,0))
        pen.setWidth(5)
        self.crossItem = self.a.scene().addPath(path, pen)

    def updateCross(self, p: QPoint):
        self.crossItem.setPos(p.x() - 10, p.y() - 10)

app = QtWidgets.QApplication(sys.argv)
window = MainWindow()
window.show()
app.exec_()
