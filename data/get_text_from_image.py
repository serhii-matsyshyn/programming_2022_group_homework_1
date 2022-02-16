""" Module to convert images to text in folder """

import os
import pytesseract
import cv2


# For windows:
# pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'


def convert_images_to_text(path_input: str, path_output: str):
    """ Converting images to text in folder """
    files = os.listdir(path_input)
    for file in files:
        if file.endswith(('.jpg', '.png', 'jpeg')):
            full_path = os.path.join(path_input, file)
            print(f'Converting image {full_path}')
            img = cv2.imread(full_path)
            text = pytesseract.image_to_string(img, lang="ukr")
            with open(f'{os.path.join(path_output, file)}.txt', 'w', encoding='utf-8') as file:
                file.write(text)


if __name__ == '__main__':
    PATH_TO_IMAGES = "images"  # Images directory path
    PATH_TO_TEXT = "text"  # Text files output path
    convert_images_to_text(PATH_TO_IMAGES, PATH_TO_TEXT)
