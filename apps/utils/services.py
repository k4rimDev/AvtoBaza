import uuid

from django.core.files import File

from PIL import Image as PILImage
from io import BytesIO


def logo_dir_path(instance, filename):
    extension = filename.split('.')[-1]
    new_filename = "announcement_%s.%s" % (uuid.uuid4(), extension)
    return new_filename

def compress_image(image):
    if image.size > 1000000:
        im = PILImage.open(image)
        im_io = BytesIO() 
        try:
            im.save(im_io, 'JPEG', quality=30) 
        except:
            im = im.convert("RGB")
            im.save(im_io, 'PNG', quality=30) 
        new_image = File(im_io, name=image.name)
    else:
        new_image = image
    return new_image

def generate_unique_id(counter):
    prefix = "AVTO"
    numeric_part = str(counter).zfill(7)
    unique_id = prefix + numeric_part
    return unique_id
