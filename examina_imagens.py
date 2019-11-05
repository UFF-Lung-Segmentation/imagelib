import numpy as np
import os
from matplotlib import pyplot as plt

# [substituir nesta seção diretório em que estão os csvs]
path = "data/220517_7/OUTPUT"

folder = os.fsencode(path)
files = os.listdir(folder)
files.sort()

slices = []

for file in files:
    filename = "{}/{}".format(path, os.fsdecode(file))
    # carrega a imagem representada em csv
    image = np.loadtxt(open(filename, "rb"), delimiter=",")
    slices.append(image)

# apresenta histograma do corte central
img_central = slices[len(slices)//2]
max = np.amax(img_central)
min = np.amin(img_central)
plt.hist(img_central.ravel(),200,[-700, -500])
plt.title("imagem central")
plt.show()

# plota todos os cortes
for idx, slice in enumerate(slices):
    plt.imshow(slice, cmap=plt.cm.bone)
    plt.title("corte: {}".format(idx))
    plt.show()

print ("Done")
