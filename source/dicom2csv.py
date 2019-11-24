import numpy
import os
import pydicom
import util

base_path ="{}/{}".format(util.config["dataset_path"], util.config["animal"])
input_path = "{}/{}".format(base_path, util.config["dicom_folder"])
output_path  = "{}/{}".format(base_path, util.config["csv_folder"])

input_folder = os.fsencode(input_path)
files = os.listdir(input_folder)
files.sort()

slices = []

for file in files:

    # le arquivos dicom
    filename = "{}/{}".format(input_path, os.fsdecode(file))
    ds = pydicom.dcmread(filename)
    b = ds.RescaleIntercept
    m = ds.RescaleSlope
    image = m * ds.pixel_array + b

    # grava arquivo csv
    # cria diretorio base
    try:
        os.makedirs(output_path)
    except:
        print(".")
    output_filename = "{}/{}{}".format(output_path, os.fsdecode(file)[:-4], ".txt")
    print(output_filename)
    image = numpy.int16(image)
    numpy.savetxt(output_filename, image, fmt="%d", delimiter=",")

print ("Done")
