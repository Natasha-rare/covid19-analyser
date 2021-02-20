import nibabel
import os
import shutil

import imageio
from PIL import Image


def convert_slice(inputfile, outputfolder, slice):
    image_array = nibabel.load(inputfile).get_fdata()
    if len(image_array.shape) == 3:
        if not os.path.exists(outputfolder):
            os.makedirs(outputfolder)
        total_slices = image_array.shape[2]
        for current_slice in range(0, total_slices):
            if current_slice == slice:
                data = image_array[:, :, current_slice]
                image_name = inputfile[:-4] + ".png"
                try:
                    imageio.imwrite(image_name, data)
                except BaseException:
                    return 0
                src = image_name
                img = Image.open(src)
                img.thumbnail((256, 256))
                img.save(src)
                shutil.move(src, outputfolder)
                return os.path.join(outputfolder, image_name.split('/')[-1])
    else:
        print('Error. Please try another file')
