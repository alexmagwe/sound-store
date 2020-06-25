import os
import secrets
from flask import current_app


def save_picture1(form_item_pic1):
    random_hex = secrets.token_hex(10)
    _, f_ext = os.path.splitext(form_item_pic1.filename)
    picture_fn = random_hex+f_ext
    picture_path = os.path.join(current_app.root_path, 'static/images', picture_fn)
    if not os.path.exists(os.path.join(current_app.root_path,'static/images')):
        print('Directory does not exist, creating one...')
        os.mkdir(os.path.join(current_app.root_path, 'static/images'))
    form_item_pic1.save(picture_path)
    print('Image Saved')
    return picture_fn

def save_picture2(form_item_pic2):
    random_hex = secrets.token_hex(10)
    _, f_ext = os.path.splitext(form_item_pic2.filename)
    picture_fn = random_hex+f_ext
    picture_path = os.path.join(current_app.root_path, 'static/images', picture_fn)
    if not os.path.exists(os.path.join(current_app.root_path,'static/images')):
        print('Directory does not exist, creating one...')
        os.mkdir(os.path.join(current_app.root_path, 'static/images'))
    form_item_pic2.save(picture_path)
    print('Image Saved')
    return picture_fn

def save_picture3(form_item_pic3):
    random_hex = secrets.token_hex(10)
    _, f_ext = os.path.splitext(form_item_pic3.filename)
    picture_fn = random_hex+f_ext
    picture_path = os.path.join(current_app.root_path, 'static/images', picture_fn)
    if not os.path.exists(os.path.join(current_app.root_path,'static/images')):
        print('Directory does not exist, creating one...')
        os.mkdir(os.path.join(current_app.root_path, 'static/images'))
    form_item_pic3.save(picture_path)
    print('Image Saved')
    return picture_fn