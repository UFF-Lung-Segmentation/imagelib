import numpy
import os
import pydicom
import util

input_path  = util.config["dicom_path"]
output_path = util.config["csv_path"]

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
    output_filename = "{}/{}{}".format(output_path, os.fsdecode(file)[:-4], ".txt")
    print(output_filename)
    image = numpy.int16(image)
    numpy.savetxt(output_filename, image, fmt="%d", delimiter=",")

print ("Done")
