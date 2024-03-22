from hashlib import sha256
import uuid
from PIL import Image, ImageDraw, ImageFont


def add_watermark_to_image(image_path):
    """Get the image path, add watermark and save it"""
    photo = Image.open(image_path)
    draw = ImageDraw.Draw(photo)
    myword = "MySite"
    w, h = photo.size
    x, y = int(w / 2), int(h / 2)
    if x > y:
        font_size = y
    else:
        font_size = x
    font = ImageFont.load_default(int(font_size/6))
    draw.text((x, y), myword, (255, 255, 255), font=font)
    photo.save(image_path)


def user_media_path(instance, filename) -> str:
    """Return user's media path with hashed filename based on hashed email and uuid4 random hash"""
    folder: str = f'user_{sha256(str(instance.email).encode("utf-8")).hexdigest()}'
    hashed_filename: str = f'{uuid.uuid4()}.{str(filename).rsplit(".")[-1]}'
    return f'{folder}/{hashed_filename}'

