import pytesseract
from PIL import Image
img_file = "page_01.jpg"
no_noise = "no_noise.jpg"

# img = Image.open(img_file)
# ocr_result = pytesseract.image_to_string(img)
# print(ocr_result)
# ***!!! computer can't read the preprocessed image !!!***

img = Image.open(no_noise)
ocr_result = pytesseract.image_to_string(img)
print(ocr_result)
