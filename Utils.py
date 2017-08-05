import io
import PIL
import requests
import gridfs
from PIL import Image
from io import BytesIO
from pymongo import MongoClient

db = MongoClient().b2w
fs = gridfs.GridFS(db)

images_json_path = 'http://54.152.221.29/images.json'
app_url = 'http://127.0.0.1:5000/'
images_path = 'img/'

small_dim = 320, 240
medium_dim = 384, 288
large_dim = 640, 480


def save_images_into_db():
    """
    Function to populate the database using a json file as seed.
    """
    image_number = 1
    for image_url in get_images_urls():
        image = requests.get(image_url)
        filename = 'b2w_image_' + str(image_number)
        save_image_into_db(filename, image.content)
        resize_and_save_image(filename, image.content)
        save_image_info(filename)
        image_number += 1


def get_images_urls():
    """
    Function to get images url from a json file.
    :return: A list with images url.
    """
    response = requests.get(images_json_path)
    data = response.json()
    return [image_url['url'] for image_url in data['images']]


def save_image_into_db(filename, image):
    """
    Function to save an image into the database.
    :param filename: Image name.
    :param image: Image to be saved into the database.
    """
    fs.put(image, filename=filename, contentType='image/jpeg')


def save_image_info(filename):
    """
    Function to save image information with all dimensions.
    :param filename: Image name.
    """
    image = {'original_image_url': app_url + images_path + filename,
             'small_image_url': app_url + images_path + filename + '_small',
             'medium_image_url': app_url + images_path + filename + '_medium',
             'large_image_url': app_url + images_path + filename + '_large'}
    images = db.images
    images.insert_one(image)


def resize_and_save_image(filename, content):
    """
    Function to resize and save an image into the database.
    :param filename: Image name.
    :param content: Image to be resized.
    """
    images = {'small': resize_image(content, small_dim),
              'medium': resize_image(content, medium_dim),
              'large': resize_image(content, large_dim)}
    for size, image in images.items():
        resized_image_filename = filename + "_" + size
        img_io = io.BytesIO()
        image.save(img_io, 'JPEG')
        img_io.seek(0)
        save_image_into_db(resized_image_filename, img_io)


def resize_image(content, dimens):
    """
    Function to resize an image.
    :param content: Image to be resized.
    :param dimens: Dimensions to resize the image.
    :return: Resized Image.
    """
    image = Image.open(BytesIO(content))
    return image.resize(dimens, PIL.Image.BICUBIC)


def get_images_from_db():
    """
    Function to get all the images from database.
    :return: All the images from database.
    """
    return db.images.find()


def get_image_from_db(image_name):
    """
    Function to get an image of the database from its name.
    :param image_name: Image name.
    :return: The most recent version of the image in GridFS.
    """
    return fs.get_last_version(filename=image_name)
