import io
from PIL import Image
from flask import Flask, jsonify, send_file

import Utils

app = Flask(__name__)


@app.route("/", methods=['GET'])
@app.route("/img", methods=['GET'])
def get_images():
    """
    Endpoint to get all the images stored in the database.
    :return: All the images stored in the database.
    """
    images = []
    for image in Utils.get_images_from_db():
        del image['_id']
        images.append(image)
    return jsonify(images)


@app.route("/img/<image_name>", methods=['GET'])
def get_image(image_name):
    """
    Endpoint to get an image stored in the database by its name.
    :param image_name: Image name.
    :return: The image itself.
    """
    return serve_image(Image.open(Utils.get_image_from_db(image_name)))


def serve_image(pil_img):
    """
    Function to provide the image.
    :param pil_img: Image to be provided.
    :return: The image itself.
    """
    img_io = io.BytesIO()
    pil_img.save(img_io, 'JPEG')
    img_io.seek(0)
    return send_file(img_io, mimetype='image/jpeg')


if __name__ == '__main__':
    Utils.save_images_into_db()
    app.run()
