# utils.py
import os
import random
import string
from werkzeug.utils import secure_filename
from PIL import Image

def save_profile_picture(form_picture):
    random_hex = ''.join(random.choices(string.ascii_lowercase + string.digits, k=8))
    _, f_ext = os.path.splitext(form_picture.filename)
    picture_filename = random_hex + f_ext
    picture_path = os.path.join(app.root_path, 'static/profile_pics', picture_filename)
    
    output_size = (125, 125)
    i = Image.open(form_picture)
    i.thumbnail(output_size)
    i.save(picture_path)

    return picture_filename
