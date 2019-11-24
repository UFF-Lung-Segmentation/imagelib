import cv2
import configparser
import datetime
import sys
import numpy as np

configparser = configparser.ConfigParser()
configparser.read('config.ini')
try:
    config = configparser['Geral']
except KeyError:
    now = datetime.datetime.now()
    msg = "Problema ao obter configuração, verifique se você está rodando o programa no diretório principal do projeto."
    print("[ERROR] {} : {}".format(now.strftime("%Y-%m-%d %H:%M:%S.%f"), msg), flush=True)
    sys.exit()

def show(imagem):
    cv2.imshow("imagem", imagem)
    cv2.waitKey()

def log(message):
    now = datetime.datetime.now()
    print("{}: {}".format(now.strftime("[LOG] %Y-%m-%d %H:%M:%S.%f"), message), flush=True)

def overlay_image(base_image, mask, solid=False):
    alpha = 0.6
    color_image = np.dstack((base_image, base_image, base_image))
    overlay = color_image.copy()
    output = color_image.copy()
    if solid == False:
        overlay[mask > 0] =  (255, 0, 0)
        cv2.addWeighted(overlay, alpha, output, 1 - alpha, 0, output)
    else:
        output[mask > 0] =  (255, 0, 0)
    return output