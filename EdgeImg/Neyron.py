import keras
import numpy as np
from PIL import Image
from tensorflow import cast, float32
import matplotlib.pyplot as plt
import os

def normalize(image):
    image = cast(image, float32)
    image = (image / 127.5) - 1
    return image

edges = np.asarray(Image.open("output.png"))
img = np.asarray(Image.open("input.jpg"))
img = normalize(img)
edges = normalize(edges)
GAB = keras.models.load_model('GABa.h5')
b = np.concatenate((img,np.asarray(edges).reshape(360,640,1)),axis=2)
t = GAB.predict(np.asarray([b]))
ans = t[0]
print(ans.shape)
ans = (((ans+1)*127.5).astype('uint8'))
tempimg1 = Image.fromarray(np.uint8(ans))
tempimg1.save("result.png")
os.remove("output.png")
os.remove("input.jpg")