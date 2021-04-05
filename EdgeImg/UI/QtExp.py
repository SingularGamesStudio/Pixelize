from PyQt5 import QtGui, QtWidgets
from PyQt5.QtCore import QPoint, pyqtSignal
class ImageLabel(QtWidgets.QLabel):
    mouseD = pyqtSignal(QPoint)
    mouseU = pyqtSignal(QPoint)
    def __init__(self, parent):
        super(ImageLabel, self).__init__(parent)
        
    def mousePressEvent(self, e):
        self.mouseD.emit(e.pos())
    def mouseReleaseEvent(self, e):
        self.mouseU.emit(e.pos())