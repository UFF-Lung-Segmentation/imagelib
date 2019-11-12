import numpy as np
import os
import util
import const

# define folder variables
dataset_folder  = util.config["dataset_path"]
animals_folders = os.listdir(os.fsencode(dataset_folder))
qtd_animals = len(animals_folders)
animals_folders.sort()

summary = "SUMMARY\n"

for i in range(qtd_animals):
    animal_name = os.fsdecode(animals_folders[i])
    region_folder = "{}/{}/{}".format(dataset_folder,animal_name,util.config["region_folder"])
    animal_folder = "{}/{}/{}".format(dataset_folder, animal_name, util.config["csv_folder"])
    if os.path.exists(region_folder):
        summary = "{}Animal: {}\n".format(summary, animal_name)

        print (summary)

        regions = os.listdir(os.fsencode(region_folder))
        regions.sort()

        animais = os.listdir(os.fsencode(animal_folder))
        animais.sort()

        hyper_aerated = 0
        norm_aerated = 0
        hypo_aerated = 0
        non_aerated = 0

        for j in range(len(regions)):
            # processa cada corte
            region_file = os.fsdecode(regions[j])
            region_file_path = "{}/{}".format(region_folder, region_file)
            region = np.loadtxt(open(region_file_path, "rb"), delimiter=",")

            animal_file = os.fsdecode(animais[j])
            animal_file_path = "{}/{}".format(animal_folder, animal_file)
            animal = np.loadtxt(open(animal_file_path, "rb"), delimiter=",")

            masked_animal = region * animal
            masked_animal[region == 0] = -3024

            hyper_aerated += len(np.where(np.logical_and(masked_animal >= const.HYPER_AERATED_MIN, masked_animal < const.HYPER_AERATED_MAX))[0])
            norm_aerated += len(np.where(np.logical_and(masked_animal >= const.NORM_AERATED_MIN, masked_animal < const.NORM_AERATED_MAX))[0])
            hypo_aerated += len(np.where(np.logical_and(masked_animal >= const.HYPO_AERATED_MIN, masked_animal < const.HYPO_AERATED_MAX))[0])
            non_aerated += len(np.where(np.logical_and(masked_animal >= const.NON_AERATED_MIN, masked_animal < const.NON_AERATED_MAX))[0])

        summary = "{} Hyper aerated: {}\n".format(summary, hyper_aerated)
        summary = "{} Norm aerated: {}\n".format(summary, norm_aerated)
        summary = "{} Hypo aerated: {}\n".format(summary, hypo_aerated)
        summary = "{} Non aerated: {}\n".format(summary, non_aerated)

print (summary)

# save_summary
summary_path = "{}/summary.txt".format(dataset_folder)
summary_file = open(summary_path, "wt")
summary_file.write(summary)
summary_file.close()