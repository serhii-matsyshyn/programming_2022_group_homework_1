import pytesseract
import cv2

# For windows:
# pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

img = cv2.imread('images/demo.jpeg')
text = pytesseract.image_to_string(img, lang="ukr")
with open('text/demo.txt', 'w', encoding='utf-8') as file:
    file.write(text)
