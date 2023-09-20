import uuid

from django.core.files import File

from PIL import Image as PILImage
from io import BytesIO


def logo_dir_path(instance, filename):
    extension = filename.split('.')[-1]
    new_filename = "announcement_%s.%s" % (uuid.uuid4(), extension)
    return new_filename

def compress_image(image):
    img = PILImage.open(image)
    im_io = BytesIO() 
    
    if image.name.split('.')[1] == 'jpeg' or image.name.split('.')[1] == 'jpg':
        img.save(im_io , format='webp', optimize=True, quality=30)
        new_image = File(im_io, name="%s.webp" %image.name.split('.')[0],)
    else:
        img.save(im_io , format='png', optimize=True, quality=30)
        new_image = File(im_io, name="%s.webp" %image.name.split('.')[0],)

    return new_image

def generate_unique_id(counter):
    prefix = "AVTO"
    numeric_part = str(counter).zfill(7)
    unique_id = prefix + numeric_part
    return unique_id

def generate_unique_id_order_items(counter):
    unique_id = str(counter).zfill(11)
    return unique_id
