from django.core.files.base import ContentFile

import os.path
from PIL import Image
from io import BytesIO
from decimal import Decimal


# сделать превью-картинку к основной
# без гордости скопировано со стака
def make_thumbnail(estate_object):
    image = Image.open(estate_object.primary_image)
    thumb_size = (300, 300)
    image.thumbnail(thumb_size)

    thumb_name, thumb_extension = os.path.splitext(estate_object.primary_image.name)
    thumb_extension = thumb_extension.lower()

    thumb_filename = thumb_name + '_thumb' + thumb_extension

    if thumb_extension in ['.jpg', '.jpeg']:
        FTYPE = 'JPEG'
    elif thumb_extension == '.gif':
        FTYPE = 'GIF'
    elif thumb_extension == '.png':
        FTYPE = 'PNG'
    else:
        return False

    temp_thumb = BytesIO()
    image.save(temp_thumb, FTYPE)
    temp_thumb.seek(0)

    estate_object.preview_image.save(thumb_filename, ContentFile(temp_thumb.read()), save=False)
    temp_thumb.close()

    return True


# валидирует ценовые значения, вычисляет скидочную цену, возвращает три значения в словаре
# скидочная цена должна быть в бэкенде, так же, как и обычная
def apply_discount(estate_default_price, estate_discount):
    default_price_float = float(estate_default_price)
    discount_float = float(estate_discount)

    if default_price_float < 0:
        default_price_float = 0
    if discount_float > 100:
        discount_float = 100
    elif discount_float < 0:
        discount_float = 0

    discounted_price_float = round(default_price_float * (1 - 0.01 * discount_float), 2)

    default_price_decimal = Decimal(default_price_float)
    discount_decimal = Decimal(discount_float)
    discounted_price_decimal = Decimal(discounted_price_float)

    data = dict()
    data['default_price'] = default_price_decimal
    data['discount'] = discount_decimal
    data['discounted_price'] = discounted_price_decimal

    return data
