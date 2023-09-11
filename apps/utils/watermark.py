import os

from PIL import ImageFont, Image, ImageDraw


class Watermark(object):
    def process(self, image):
        text = 'AVTOBAZA.AZ'
        if bool(os.getenv("DEBUG")):
            font = ImageFont.truetype('/Users/kerimmirzequliyev/Desktop/my_work/AvtoBaza/static/DejaVu_Sans/DejaVuSans-Bold.ttf', 36)
        else:
            font = ImageFont.truetype('/usr/share/fonts/dejavu/DejaVuSans-Bold.ttf', 36)
        rgba_image = image.convert('RGBA')
        text_overlay = Image.new('RGBA', rgba_image.size, (255, 255, 255, 0))
        image_draw = ImageDraw.Draw(text_overlay)
        text_size_x, text_size_y = image_draw.textsize(text, font=font)
        text_xy = ((rgba_image.size[0] / 2) - (text_size_x / 2), (rgba_image.size[1] / 2) - (text_size_y / 2))
        image_draw.text(text_xy, text, font=font, fill=(255, 255, 255, 128))
        image_with_text_overlay = Image.alpha_composite(rgba_image, text_overlay)
        return image_with_text_overlay
