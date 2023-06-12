import io
from PIL import Image
from django.core.files.uploadedfile import InMemoryUploadedFile


def get_optimized_image(
        image: object, image_name: str, quality: int,
        ext: str, size=None):
    i = Image.open(image).convert('RGB')
    thumb_io = io.BytesIO()
    if size:
        i.thumbnail(size)
        i = i.resize(size)
    i.save(thumb_io, format='JPEG', quality=quality)
    image = InMemoryUploadedFile(
        thumb_io, None, image_name, ext, thumb_io.tell(), None)
    return image
