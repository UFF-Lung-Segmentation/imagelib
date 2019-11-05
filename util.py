import cv2
import configparser
import datetime
import sys

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

