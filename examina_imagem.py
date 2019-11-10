import numpy as np
import os
from matplotlib import pyplot as plt
import util

path = util.config["region_path"]

CORTE = 63
MIN_VALUE = 0
MAX_VALUE = 1

folder = os.fsencode(path)
files = os.listdir(folder)
files.sort()

for idx, file in enumerate(files):
    if (idx == CORTE):
        filename = "{}/{}".format(path, os.fsdecode(file))

image = np.loadtxt(open(filename, "rb"), delimiter=",")

# apresenta histograma do corte
max = np.amax(image)
min = np.amin(image)
plt.hist(image.ravel(), 200, [MIN_VALUE, MAX_VALUE])
plt.title("imagem")
plt.show()

plt.imshow(image, cmap=plt.cm.bone)
plt.title("corte: {}".format(idx))
plt.show()

print ("Done")
