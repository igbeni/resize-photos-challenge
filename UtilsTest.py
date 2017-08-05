import unittest
import os
import Utils
from Utils import get_images_urls, resize_image

test_images_folder = "test_images/"


class UtilsTest(unittest.TestCase):
    def image_urls_amount(self):
        """
        Test for the amount of urls read from the json file.
        """
        self.assertEqual(len(get_images_urls()), 10)

    def resize_image_small(self):
        """
        Testing image resizing to small size.
        """
        for image in os.listdir(test_images_folder):
            file = open(test_images_folder + image, 'rb')
            resized_image = resize_image(file.read(), Utils.small_dim)
            width, height = resized_image.size

            self.assertEqual((width, height), Utils.small_dim)

    def resize_image_medium(self):
        """
        Testing image resizing to medium size.
        """
        for image in os.listdir(test_images_folder):
            file = open(test_images_folder + image, 'rb')
            resized_image = resize_image(file.read(), Utils.medium_dim)
            width, height = resized_image.size

            self.assertEqual((width, height), Utils.medium_dim)

    def resize_image_large(self):
        """
        Testing image resizing to large size.
        """
        for image in os.listdir(test_images_folder):
            file = open(test_images_folder + image, 'rb')
            resized_image = resize_image(file.read(), Utils.large_dim)
            width, height = resized_image.size

            self.assertEqual((width, height), Utils.large_dim)

    def generate_resized_images(self):
        """
        Testing the creation of resized images.
        """
        content = open(test_images_folder + "image0.jpg", 'rb').read()
        resized_images = {'small': resize_image(content, Utils.small_dim),
                          'medium': resize_image(content, Utils.medium_dim),
                          'large': resize_image(content, Utils.large_dim)}
        self.assertEqual(resized_images['small'].size, Utils.small_dim)
        self.assertEqual(resized_images['medium'].size, Utils.medium_dim)
        self.assertEqual(resized_images['large'].size, Utils.large_dim)


if __name__ == '__main__':
    unittest.main()
