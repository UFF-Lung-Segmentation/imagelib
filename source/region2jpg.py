import numpy as np
import os
import imageio
import util
import sys
import cv2

WINDOW_LENGHT=-100
WINDOW_WIDTH=1220

MIN_DICOM=-1024
MAX_DICOM=1024

# define folder variables
base_path ="{}/{}".format(util.config["dataset_path"], util.config["animal"])
image_folder  = "{}/{}".format(base_path, util.config["csv_folder"])
region_folder = "{}/{}".format(base_path, util.config["region_folder"])
output_folder = "{}/{}".format(base_path, util.config["jpg_folder"])

image_files = os.listdir(os.fsencode(image_folder))
qtd_images = len(image_files)
image_files.sort()

region_files = os.listdir(os.fsencode(region_folder))
qtd_region = len(region_files)
region_files.sort()

if qtd_images != qtd_region:
    util.log("number of image and region files must be the same, it is currently: {} and {}".format(qtd_images, qtd_region))
    sys.exit(-1)

# verifica se diretorio de saida existe, senao cria
if not os.path.exists(output_folder):
    os.makedirs(output_folder)

# load text files from filesystem and merge image and region (mask) files
slices = []

for i in range(qtd_images):
    image_filename = os.fsdecode(image_files[i])
    region_filename = os.fsdecode(region_files[i])
    if (image_filename.find(".csv") > 0) or (image_filename.find(".txt") > 0):
    # if (i == 0):
        util.log("processando corte {}".format(image_filename))
        # carrega a imagem
        image_filepath = "{}/{}".format(image_folder, image_filename)
        image = np.loadtxt(open(image_filepath, "rb"), delimiter=",")

        image = image.astype("int16")
        image = np.clip(image, MIN_DICOM, MAX_DICOM)

        # carrega regiao
        region_filepath = "{}/{}".format(region_folder, region_filename)
        region = np.loadtxt(open(region_filepath, "rb"), delimiter=",")
        region = region.astype("uint8")
        area_regiao = np.sum(region)

        # normaliza imagem
        min_window = WINDOW_LENGHT - (WINDOW_WIDTH // 2)
        if min_window < MIN_DICOM: min_window = MIN_DICOM

        max_window = WINDOW_LENGHT + (WINDOW_WIDTH // 2)
        if max_window > MAX_DICOM: max_window = MAX_DICOM

        normalized = image.copy()
        normalized[normalized >= max_window] = max_window
        normalized[normalized < min_window] = min_window

        # normaliza em tons de cinza
        for cell in np.nditer(normalized, op_flags=['readwrite']):
            cell[...] = ((cell - min_window) * 255) // (max_window - min_window)
        gray = normalized.astype('uint8')

        # aplica a máscara
        masked_image = util.overlay_image(gray, region, False)

        # inclui texto com a área
        cv2.putText(masked_image, "region area={}".format(area_regiao), (10, 30), cv2.FONT_HERSHEY_DUPLEX, 0.6, (255, 255, 255), lineType=cv2.LINE_AA)

        # inclui texto com o número do slide
        cv2.putText(masked_image, "{}".format(os.fsdecode(image_filename[8:-4])), (225, 30), cv2.FONT_HERSHEY_DUPLEX, 0.6, (255, 255, 255), lineType=cv2.LINE_AA)

        # salva imagem como jpg
        output_filepath = "{}/{}.jpg".format(output_folder, os.fsdecode(image_filename[:-4]))
        imageio.imwrite(output_filepath, masked_image)


output_video_path = "{}/{}.mp4".format(output_folder, util.config["animal"])
ffmpeg = "ffmpeg -r 1 -i {}/IM-0001-%04d.jpg -vcodec mpeg4 -y {}".format(output_folder, output_video_path)
os.system(ffmpeg)

print ("Done")
