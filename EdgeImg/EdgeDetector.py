import numpy as np
from scipy.ndimage.filters import convolve
from collections import deque
#import cpp

class EdgeDetector:
    def __init__(self, sigma = 8, blur = 3, gradKernel = [[3, 10, 3], [0, 0, 0], [-3, -10, -3]], lowP = 0.005, highP = 0.12, trash = 20):
        self.sigma = sigma
        self.noiseIntensity = blur*2+1
        self.gradKernel = gradKernel
        self.lowP = lowP
        self.highP = highP
        self.trashSz = trash
        return
    def createGaussKernel(self):
        sz = self.noiseIntensity
        k = np.zeros((sz, sz))
        for i in range(sz):
            for j in range(sz):
                k[i][j] = (1/(np.pi*self.sigma))*np.exp(-((i-(int(sz))//2)**2+(j-(int(sz))//2)**2)/self.sigma)
        return k
    def calcGradient(self, img):
        xKernel = self.gradKernel
        yKernel = np.rot90(xKernel)
        xGrad = convolve(img, xKernel)
        yGrad = convolve(img, yKernel)
        Grad = np.sqrt(xGrad**2+yGrad**2)
        ang = np.arctan2(yGrad, xGrad)
        Grad = Grad.astype(int)
        Grad = Grad / Grad.max() * 255
        n, m = Grad.shape
        res = np.zeros((n, m))
        for i in range(1, n-1):
            for j in range(1, m-1):
                res[i][j] = Grad[i][j]
                r1 = 0
                r2 = 0
                while ang[i][j] < 0:
                    ang[i][j]+=2*np.pi
                if ang[i][j]>np.pi:
                    ang[i][j]-=np.pi
                if (ang[i][j]<np.pi/8) or (ang[i][j]>=np.pi/8*7):
                    r1 = Grad[i+1][j]
                    r2 = Grad[i-1][j]
                elif (ang[i][j]<np.pi/8*3) and (ang[i][j]>=np.pi/8):
                    r1 = Grad[i+1][j+1]
                    r2 = Grad[i-1][j-1]
                elif (ang[i][j]<np.pi/8*5) and (ang[i][j]>=np.pi/8*3):
                    r1 = Grad[i][j+1]
                    r2 = Grad[i][j-1]
                else:
                    r1 = Grad[i+1][j-1]
                    r2 = Grad[i-1][j+1]
                if Grad[i][j]<max(r1, r2):
                    res[i][j] = 0
        return res
    def threshold(self, img):
        high = img.max()*self.highP
        low = img.max()*self.lowP
        strong1, strong2 = np.where(img>=high)
        weak1, weak2 = np.where((img<high) & (img>=low))
        n, m = img.shape
        res = np.zeros((n, m))
        res[strong1, strong2] = 255;
        t1 = weak1.shape
        for x in range(t1[0]):
            i = weak1[x]
            j = weak2[x]
            if i!=0 and i!=n-1 and j!=0 and j!=m-1:
                cnt = 0
                for i1 in range(-1, 2):
                    for j1 in range(-1, 2):
                        if not(i1==0 and j1==0):
                            if res[i+i1][j+j1] == 255:
                                cnt+=1
                if cnt>0:
                    res[i][j] == 255
        return res
    def deleteTrash(self, img):
        n, m = img.shape
        res = np.copy(img)
        used = np.zeros((n, m))
        for i in range(n):
            for j in range(m):
                if img[i][j] == 255 and used[i][j]==0:
                    e = []
                    e.append((i, j))
                    bfs = deque()
                    used[i][j] = 1
                    bfs.append((i, j))
                    while len(bfs)>0:
                        i1, j1 = bfs.popleft()
                        for i2 in range(-1, 2):
                            for j2 in range(-1, 2):
                                if i1+i2<n and j1+j2<m and i1+i2>=0 and j1+j2>=0 and used[i1+i2][j1+j2]==0 and img[i1+i2][j1+j2]==255 :
                                    bfs.append((i1+i2, j1+j2))
                                    e.append((i1+i2, j1+j2))
                                    used[i1+i2][j1+j2] = 1
                    if len(e)<self.trashSz:
                        for i1, j1 in e:
                            res[i1][j1] = 0
        return res
    def connect(self, img, base):
        inp = base
        n, m = img.shape
        low = base.max()*self.lowP
        for i in range(n):
            for j in range(m):
                inp[i][j] = base[i][j];
                if img[i][j]>0:
                    inp[i][j] = 10000
                #if base[i][j]<=low:
                 #   inp[i][j] = 0
        res = inp
        #res = cpp.enclose(inp)
        return res
    def gaussBlur(self, img):
        gauss = self.createGaussKernel()
        blured = convolve(img, gauss)
        return blured
    def proceed(self, img):
        res = self.threshold(img)
        res = self.deleteTrash(res)
        #res = self.connect(res, img);
        return res