# Using the preprocessed image in Image Preprocess directory
import pytesseract
from PIL import Image
img_file = "page_01.jpg"
no_noise = "no_noise.jpg"

img = Image.open(no_noise)
ocr_result = pytesseract.image_to_string(img)
print(ocr_result)
