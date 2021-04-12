from EdgeDetector import EdgeDetector as ED
from resize import Resize
import utils
import numpy as np
import keyboard
import sys
from PyQt5.QtWidgets import *
from PyQt5.QtGui import QPixmap, QImage, QColor, QColorConstants
from UI import first, second, third
from PIL import Image
from PIL.ImageQt import ImageQt
from PyQt5.QtCore import Qt, QPoint

global img0
global blured
global res
global parser
global resizer
global window
global imgloaded
global ac3
class App(QMainWindow):
    def __init__(self, parent = None):
        super(App, self).__init__(parent)
        self.form_widget = Win1(self) 
        self.setCentralWidget(self.form_widget)
        self.showMaximized()

class Win3(QWidget, third.Ui_StartForm):
    def __init__(self, parent):
        global ac3
        global blured
        ac3 = True
        super(Win3, self).__init__(parent)
        self.setupUi(self)
        self.area = [-1, -1, -1, -1]
        self.st = []
        self.grad = parser.calcGradient(blured)
        self.calc()
        self.HighVal.valueChanged.connect(self.updateSliders)
        self.LowVal.valueChanged.connect(self.updateSliders)
        self.DoButton.clicked.connect(self.calc)
        self.BackBtn.clicked.connect(self.back)
        self.Image.mouseD['QPoint'].connect(self.mouseDown)
        self.Image.mouseU['QPoint'].connect(self.mouseUp)
        self.choosing = True
        #self.NextBtn.clicked.connect(self.next)
    def updateSliders(self):
        parser.highP = self.HighVal.value()/1000
        parser.lowP = self.LowVal.value()/1000
        self.High.setText("High treshold: "+str(self.HighVal.value()))
        if self.HighVal.value()>=self.LowVal.value():
            self.Low.setText("Low treshold: "+str(self.LowVal.value()))
        else:
            self.Low.setText("ERROR: High must be higher than Low")
    def mouseDown(self, pos):
        if self.choosing:
            self.dragS = pos
    def mouseUp(self, pos):
        if self.choosing:
            self.area = [self.dragS.x(), self.dragS.y(), pos.x(), pos.y()]
            if self.area[0]>0 and self.area[1]>0 and self.area[2]>0 and self.area[3]>0 and self.area[0]<=self.img2.size().width() and self.area[1]<=self.img2.size().height() and self.area[2]<=self.img2.size().width() and self.area[3]<=self.img2.size().height():
                img3 = self.img2.copy(self.img2.rect())
                if self.area[0]!=self.area[2] and self.area[1]!=self.area[3]:
                    for i in range(min(self.area[0], self.area[2]),max(self.area[0], self.area[2])):
                        img3.setPixelColor(i, min(self.area[1], self.area[3]), QColorConstants.Red)
                        img3.setPixelColor(i, max(self.area[1], self.area[3])-1, QColorConstants.Red)
                    for j in range(min(self.area[1], self.area[3]),max(self.area[1], self.area[3])):
                        img3.setPixelColor(min(self.area[0], self.area[2]), j, QColorConstants.Red)
                        img3.setPixelColor(max(self.area[0], self.area[2])-1, j, QColorConstants.Red)
                pixmap = QPixmap.fromImage(img3)
                self.Image.setPixmap(pixmap)
                self.Image.resize(pixmap.width(), pixmap.height())
                #self.choosing = False
    def undo(self):
        global res
        print(len(self.st))
        if len(self.st)>1:
            self.st.pop()
            res = self.st[len(self.st)-1]
            tempimg1 = Image.fromarray(np.uint8(res))
            self.img2 = ImageQt(tempimg1).convertToFormat(QImage.Format.Format_RGB888)
            pixmap = QPixmap.fromImage(self.img2)
            self.Image.setPixmap(pixmap)
            self.Image.resize(pixmap.width(), pixmap.height())
    def calc(self):
        global parser
        global resizer
        global res
        if self.HighVal.value()>=self.LowVal.value():
            if self.area[0]==self.area[2] or self.area[1]==self.area[3]:
                res = parser.proceed(self.grad)
                res = resizer.proceed(res);
                tempimg1 = Image.fromarray(np.uint8(res))
                self.img2 = ImageQt(tempimg1).convertToFormat(QImage.Format.Format_RGB888)
                tempimg1.save("output.png")
                pixmap = QPixmap.fromImage(self.img2)
                self.Image.setPixmap(pixmap)
                self.Image.resize(pixmap.width(), pixmap.height())
            else:
                subm = self.grad[min(self.area[1], self.area[3]):max(self.area[1], self.area[3]), min(self.area[0], self.area[2]):max(self.area[0], self.area[2])]
                now = parser.proceed(subm)
                x, y = res.shape
                w = [i*y+j for j in range(max(self.area[0], self.area[2])-1, min(self.area[0], self.area[2])-1, -1) for i in range(min(self.area[1], self.area[3]),max(self.area[1], self.area[3]))]
                now = np.rot90(now, 1)
                np.put(res, w, now)
                tempimg1 = Image.fromarray(np.uint8(res))
                tempimg1.save("output.png")
                self.img2 = ImageQt(tempimg1).convertToFormat(QImage.Format.Format_RGB888)
                pixmap = QPixmap.fromImage(self.img2)
                self.Image.setPixmap(pixmap)
                self.Image.resize(pixmap.width(), pixmap.height())
        self.st.append(np.copy(res))
    def back(self):
        global ac3
        global window
        ac3 = False
        window.form_widget = Win2(window) 
        window.setCentralWidget(window.form_widget)
    def next(self):
        global window
        window.form_widget = Win3(window)
        window.setCentralWidget(window.form_widget)

class Win2(QWidget, second.Ui_StartForm):
    def __init__(self, parent):
        global img0
        super(Win2, self).__init__(parent)
        self.setupUi(self)
        self.updateSliders()
        self.blur()
        self.SizeVal.valueChanged.connect(self.updateSliders)
        self.SigmaVal.valueChanged.connect(self.updateSliders)
        self.GoBtn.clicked.connect(self.blur)
        self.BackBtn.clicked.connect(self.back)
        self.NextBtn.clicked.connect(self.next)
    def updateSliders(self):
        parser.sigma = self.SigmaVal.value()/10
        parser.noiseIntensity = 2*self.SizeVal.value()+1
        self.Sigma.setText("Sigma: "+str(self.SigmaVal.value()))
        self.Size.setText("Size: "+str(self.SizeVal.value()))
    def blur(self):
        global img0
        global parser
        global blured
        blured = parser.gaussBlur(img0)
        tempimg1 = Image.fromarray(np.uint8(blured))
        tempimg2 = ImageQt(tempimg1)
        pixmap = QPixmap.fromImage(tempimg2)
        self.Image.setPixmap(pixmap)
        self.Image.resize(pixmap.width(), pixmap.height())
    def back(self):
        global window
        window.form_widget = Win1(window) 
        window.setCentralWidget(window.form_widget)
    def next(self):
        global window
        window.form_widget = Win3(window)
        window.setCentralWidget(window.form_widget)

class Win1(QWidget, first.Ui_StartForm):
    def __init__(self, parent):
        super(Win1, self).__init__(parent)
        self.setupUi(self)
        self.ChooseBtn.clicked.connect(self.openImage)
        self.NextBtn.clicked.connect(self.next)
    def openImage(self):
        global img0
        global parser
        global imgloaded
        str, temp = QFileDialog.getOpenFileName(self, "Open Image", "", "*.png *.jpg");
        img0 = utils.load_data(str)
        imgloaded = True
        tempimg1 = Image.fromarray(np.uint8(img0))
        tempimg2 = ImageQt(tempimg1)
        pixmap = QPixmap.fromImage(tempimg2)
        self.Image.setPixmap(pixmap)
        self.Image.resize(pixmap.width(), pixmap.height())
    def next(self):
        global window
        global imgloaded
        if imgloaded:
            window.form_widget = Win2(window) 
            window.setCentralWidget(window.form_widget)

def QImageFromNP(img):
    height, width = img.shape
    res = QImage(img.data, height, width, width, QImage.Format_Grayscale8)
    return res
def ctz():
    global window
    global ac3
    if ac3==True:
        window.form_widget.undo()
def main():
    global ac3
    global window
    global parser
    global resizer
    global img0
    ac3 = False
    keyboard.add_hotkey('Ctrl + Z', ctz)
    imgloaded = False
    parser = ED()
    resizer = Resize()
    app = QApplication(sys.argv)
    window = App()
    window.show()
    app.exec_()

if __name__ == '__main__':
    main()