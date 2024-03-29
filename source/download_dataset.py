#!/usr/bin/python3
import urllib.request, urllib.parse, urllib.error
import xml.etree.ElementTree as ET
import os
import sys

# Downloads bucket contents
# A command line argument with file extension can be used in case you want to download only specific types
# Example:
# To download only dicom files: python3 download_dataset.py dcm
# To download only txt (csv) files: python3 download_dataset.py txt

BUCKET_URL = 'http://ratos.s3-sa-east-1.amazonaws.com/'
DATASET_FOLDER = 'dataset/'

def download_arquivo(file, file_type, animal, count):
    tamanho = len(file)
    local_filename = "{}{}".format(DATASET_FOLDER, file)
    animal_remoto = file[:file.find('/')]
    file_type_remoto = file[-3:]

    # verifica se deve baixar o item atual
    download = False
    if (file[tamanho - 1] == '/'):
        download = False
    elif (file_type == "all") and (animal == "all"):
        download = True
    elif ((file_type == "all") and (animal == animal_remoto)):
        download = True
    elif ((file_type == file_type_remoto) and (animal == "all")):
        download = True
    elif ((file_type == file_type_remoto) and (animal == animal_remoto)):
        download = True

    if download:
        url = "{}{}".format(BUCKET_URL, file)
        if os.path.exists(local_filename):
            print(count, " Arquivo %s ja existe" % local_filename)
        else:
            os.makedirs(os.path.dirname(local_filename), exist_ok=True)
            urllib.request.urlretrieve(url, local_filename)
            print(count, " Baixou arquivo %s com sucesso" % local_filename)


if __name__ == '__main__':
    # define qual tipo de arquivos vai baixar e o animal
    file_type = "all"
    animal = "all"
    if len(sys.argv) >= 2:
        file_type = sys.argv[1]
    if len(sys.argv) >= 3:
        animal = sys.argv[2]
    count = 0

    # tratamento paginacao
    truncated = True
    last_file = None

    while (truncated):
        # faz o download do bucket
        url = BUCKET_URL
        if last_file != None:
            url = "{}?marker={}".format(BUCKET_URL, last_file)
        url = urllib.request.urlopen(url)
        data = url.read()
        # print(data.decode())
        tree = ET.fromstring(data.decode())

        # tratamento para paginacao
        for child in tree:
            tag = child.tag
            if tag.find("IsTruncated") > 0:
                if child.text == "true":
                    truncated = True
                else:
                    truncated = False
                break

        for child in tree:
            for grandson in child:
                tag = grandson.tag
                if tag != None:
                    if tag.find("Key") > 0:
                        file = grandson.text
                        last_file = file
                        if (file != None) and (file.find("index.html") < 0):
                            count += 1
                            download_arquivo(file, file_type, animal, count)

    print("Done")