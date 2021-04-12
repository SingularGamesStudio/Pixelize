import numpy as np

class Resize:
    def __init__(self, _k = 2):
        self.k = _k
        return
    def div2(self, img):
        n, m = img.shape
        n//=2
        m//=2
        res = np.zeros((n, m))
        for i in range(0, n):
            for j in range(0, m):
                cnt = 0
                if img[2*i][2*j]>0:
                    cnt+=1
                if img[2*i+1][2*j]>0:
                    cnt+=1
                if img[2*i][2*j+1]>0:
                    cnt+=1
                if img[2*i+1][2*j+1]>0:
                    cnt+=1
                if cnt>=2:
                    res[i][j] = 255;
                if cnt==1:
                    res[i][j] = 122;
        return res
    def deleteSmallAreas(self, img):
        n, m = img.shape
        res = np.copy(img)
        small = np.zeros((n, m))
        for i in range(0, n):
            for j in range(0, m):
                if img[i][j]==0:
                    dup = -1
                    for p in range(3, 0, -1):
                        if i+p<n and img[i+p][j]>0:
                            dup = p;
                    ddown = -1
                    for p in range(3, 0, -1):
                        if i-p>=0 and img[i-p][j]>0:
                            ddown = p;
                    dright = -1
                    for p in range(3, 0, -1):
                        if j+p<m and img[i][j+p]>0:
                            dright = p;
                    dleft = -1
                    for p in range(3, 0, -1):
                        if j-p>=0 and img[i][j-p]>0:
                            dleft = p;
                    if (dright>0 and dleft>0) or (dup>0 and ddown>0):
                        small[i][j] = 1
        used = np.zeros((n, m))
        for i in range(0, n):
            for j in range(0, m):
                if used[i][j]==0:
                    dfs = [(i, j)]
                    sz = 0
                    cnt = 0
                    used[i][j] = 1
                    while dfs.count>0:
                        x, y = dfs[dfs.count-1]
                        dfs.pop()
                        sz+=1
                        if small[x][y]>0:
                            cnt+=1
                        if x+1<n and used[x+1][y]==0 and img[x+1][y]>0:
                            dfs.append((x+1, y))
                            used[x+1][y] = 1
                        if y+1<m and used[x][y+1]==0 and img[x][y+1]>0:
                            dfs.append((x, y+1))
                            used[x][y+1] = 1
                        if x-1>=0 and used[x-1][y]==0 and img[x-1][y]>0:
                            dfs.append((x-1, y))
                            used[x-1][y] = 1
                        if y-1>=0 and used[x][y-1]==0 and img[x][y-1]>0:
                            dfs.append((x, y-1))
                            used[x][y-1] = 1
    def proceed(self, img):
        res = img
        for i in range(0, self.k):
            res = self.div2(res)
        return res