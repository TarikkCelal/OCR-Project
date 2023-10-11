import pytesseract
import cv2
image = cv2.imread("sample_mgh.jpeg")
im_h, im_w, im_d = image.shape
base_image = image.copy()

# Preprocessing the image
gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
blur = cv2.GaussianBlur(gray, (7, 7), 0)
thresh = cv2.threshold(blur, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)[1]
kernal = cv2.getStructuringElement(cv2.MORPH_RECT, (50, 10))
dilate = cv2.dilate(thresh, kernal, iterations=1)

cv2.imwrite("sample_dilated.jpg", dilate)

# Making the image ready for bounding boxes
cnts = cv2.findContours(dilate, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
cnts = cnts[0] if len(cnts) == 2 else cnts[1]
cnts = sorted(cnts, key=lambda x: cv2.boundingRect(x)[1])

# This step is for cutting footnote's boxes so only main text will remain
for c in cnts:
    x, y, w, h = cv2.boundingRect(c)
    if h < 20 and w > 250:
        roi = base_image[0:y+h, 0:x+im_w]
        cv2.rectangle(image, (x, y), (x+w, y+h), (36, 255, 12), 2)

cv2.imwrite("output_without_footnotes.jpg", roi)

ocr_result = pytesseract.image_to_string(roi)
print(ocr_result)