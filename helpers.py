import os
from playlib import app

def get_image(id):
    for filename in os.listdir(app.config['UPLOAD_PATH']):
        if f'cover{id}' in filename:
            return filename


def delete_cover(id):
    file = get_image(id)
    os.remove(os.path.join(app.config['UPLOAD_PATH'],file))