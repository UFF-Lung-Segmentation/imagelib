import numpy as np
import os
import imageio
import util

# [substituir nesta seção diretórios de entrada e saída]
segmented_folder  = util.config["output_path"]
output_folder = util.config["jpg_path"]

input_folder_enconded = os.fsencode(segmented_folder)
output_folder_enconded = os.fsencode(output_folder)
input_files = os.listdir(input_folder_enconded)
input_files.sort()

slices = []

# verifica se diretorio de saida existe, senao cria
if not os.path.exists(output_folder):
    os.makedirs(output_folder)

# carrega as imagens csv a partir do filesystem
for filename in input_files:
    input_filename = os.fsdecode(filename)
    if (input_filename.find(".csv") > 0) or (input_filename.find(".txt") > 0):

        # carrega a imagem
        input_filepath = "{}/{}".format(segmented_folder, os.fsdecode(input_filename))
        image = np.loadtxt(open(input_filepath, "rb"), delimiter=",")
        image = image.astype("int16")
        image = np.clip(image, -1024, 1024)

        # salva imagem como jpg
        output_filepath = "{}/{}.jpg".format(output_folder, os.fsdecode(input_filename[:-4]))
        imageio.imwrite(output_filepath, image)


print ("Done")
