from typing import Callable

import numpy as np
from PyQt5.QtCore import QPoint, Qt, QCoreApplication
from PyQt5.QtGui import QPixmap, QPainterPath, QPen, QColor, QImage
from PyQt5.QtWidgets import QGraphicsView, QLabel, QGraphicsScene, QGraphicsPixmapItem, QSlider
from spectral import open_image, get_rgb
from spectral.io.bilfile import BilFile

from gui.hyperspectralImgModel import HyperspectralImgModel


class SelectionPanelController:
    def __init__(self, graphicsView: QGraphicsView, result: QLabel, pixelPos: QLabel, zoomSlider: QSlider, *args, **kwargs):
        self.graphicsView = graphicsView
        self.graphicsView.setScene(QGraphicsScene())
        self.graphicsView.setViewportUpdateMode(QGraphicsView.FullViewportUpdate)
        self.graphicsView.mousePressEvent = self.onSceneClick
        self.scaleFactor = 1
        self.onImgClickCallback = None
        self.onImgLoadedCallback = None
        self.imgItem = None
        self.crossItem = None
        self.resultLabel = result
        self.pixelPos = pixelPos
        self.zoomSlider = zoomSlider
        zoomSlider.valueChanged.connect(self.__onZoomChanged)

    def setOnImgClick(self, fn):
        self.onImgClickCallback = fn

    def setOnImgLoaded(self, fn: Callable[[HyperspectralImgModel], None]):
        self.onImgLoadedCallback = fn

    def __raiseOnImgClick(self, p: QPoint):
        if self.onImgClickCallback is not None:
            self.onImgClickCallback(p)

    def __raiseOnImgLoaded(self, model: HyperspectralImgModel):
        if self.onImgLoadedCallback is not None:
            self.onImgLoadedCallback(model)

    def __onZoomChanged(self, val):
        self.scaleImg(val)

    def scaleImg(self, factor):
        img = self.hyperspectralImg.sceneImg
        p = QPixmap.fromImage(img.scaled(img.size().width() * factor,
                                                    img.size().height() * factor), Qt.AutoColor)
        self.graphicsView.scene().removeItem(self.imgItem)
        self.graphicsView.mousePressEvent = self.onSceneClick
        self.imgItem: QGraphicsPixmapItem = self.graphicsView.scene().addPixmap(p)
        self.scaleFactor = factor
        self.renderCrosshair()

    def renderCrosshair(self):
        if self.crossItem is not None:
            self.graphicsView.scene().removeItem(self.crossItem)
        path = QPainterPath()
        path.moveTo(10, 0)
        path.lineTo(10, + 20)
        path.moveTo(0, 10)
        path.lineTo(20, 10)

        pen = QPen(QColor(255, 0, 0))
        pen.setWidth(1.5 * self.scaleFactor if 2 * self.scaleFactor < 5 else 5)
        self.crossItem = self.graphicsView.scene().addPath(path, pen)
        self.pixelPos.setText("")

    def updateCrosshair(self, p: QPoint):
        self.crossItem.setPos(p.x() - 10, p.y() - 10)

    def onSceneClick(self, event):
        point = event.pos()
        item = self.graphicsView.itemAt(point)
        if item is None:
            pass
        scenePoint = self.graphicsView.mapToScene(point)
        mapped = self.imgItem.mapFromScene(scenePoint)
        imgPoint = QPoint(mapped.x() / self.scaleFactor, mapped.y() / self.scaleFactor)
        self.updateCrosshair(scenePoint)
        self.pixelPos.setText("x: %d y: %d" % (imgPoint.x(), imgPoint.y()))
        QCoreApplication.processEvents()
        self.__raiseOnImgClick(imgPoint)

    def loadImg(self, filePath: str):
        if self.imgItem is not None:
            self.graphicsView.scene().removeItem(self.imgItem)
            self.resultLabel.clear()
            self.resultLabel.setText("Click on img")
        self.prevPoint = None
        file: BilFile = open_image(filePath)
        rgb = get_rgb(file)
        rgb = rgb * 255
        rgb = rgb.astype(np.uint8)
        loadedImg = QImage(rgb.tobytes(), rgb.shape[0], rgb.shape[1], rgb.shape[0] * 3, QImage.Format_RGB888)

        self.hyperspectralImg = HyperspectralImgModel(file, loadedImg)
        self.__raiseOnImgLoaded(self.hyperspectralImg)

        p = QPixmap.fromImage(loadedImg, Qt.AutoColor)
        self.imgItem: QGraphicsPixmapItem = self.graphicsView.scene().addPixmap(p)
        self.scaleImg(self.zoomSlider.value())


    def displayResult(self, img: QImage):
        imgw = self.imgItem.pixmap().width()
        imgh = self.imgItem.pixmap().height()

        destW = self.imgItem.pixmap().width() if self.resultLabel.size().width() > imgw \
            else self.resultLabel.size().width()
        destH = self.imgItem.pixmap().height() if self.resultLabel.size().height() > imgh \
            else self.resultLabel.size().height()
        sw = destW
        sh = destH

        if img.width() * sh > sw * img.height():
            destH = sw * img.height() / img.width()
        else:
            destW = sh * img.width() / img.height()
        p = QPixmap.fromImage(img.scaled(destW, destH))
        self.resultLabel.setPixmap(p)
        self.resultLabel.setMask(p.mask())