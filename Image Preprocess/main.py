import cv2
from matplotlib import pyplot as plt

image_file = "page_01.jpg"
img = cv2.imread(image_file)


def display(im_path):
    dpi = 80
    im_data = plt.imread(im_path)

    height, width = im_data.shape[:2]

    # What size does the figure need to be in inches to fit the image?
    figsize = width / float(dpi), height / float(dpi)

    # Create a figure of the right size with one axes that takes up the full figure
    fig = plt.figure(figsize=figsize)
    ax = fig.add_axes([0, 0, 1, 1])

    # Hide spines, ticks, etc.
    ax.axis('off')

    # Display the image.
    ax.imshow(im_data, cmap='gray')

    plt.show()


# DISPLAY---------------
#display(image_file)


# INVERT------------------------------------
inverted_image = cv2.bitwise_not(img)
cv2.imwrite("inverted.jpg", inverted_image)
#display("inverted.jpg")


# GRAYSCALE FOR MORE VISIBLE IMAGE----------------------------------------------
# before making the image black and white, turn it to gray for better results
def grayscale(image):
    return cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)


gray_image = grayscale(img)
cv2.imwrite("gray.jpg", gray_image)
#display("gray.jpg")


# BLACK AND WHITE IMAGE--------------------------------------------------
# integers are important parameters to make the image more visible
thresh, im_bw = cv2.threshold(gray_image, 212, 230, cv2.THRESH_BINARY)
cv2.imwrite("bw_image.jpg", im_bw)
#display("bw_image.jpg")


# REMOVING THE NOISE-----------------------------------------------------
# makes the image a little harder to read so don't use it unless you need
def noise_removal(image):
    import numpy as np
    kernel = np.ones((1, 1), np.uint8)
    image = cv2.dilate(image, kernel, iterations=1)
    kernel = np.ones((1, 1), np.uint8)
    image = cv2.erode(image, kernel, iterations=1)
    image = cv2.morphologyEx(image, cv2.MORPH_CLOSE, kernel)
    image = cv2.medianBlur(image, 3)
    return image


no_noise = noise_removal(im_bw)
cv2.imwrite("no_noise.jpg", no_noise)
#display("no_noise.jpg")


# DILATION AND EROSION
# dilation is for make the letters thicker
# erosion is for make the letters thinner
def thin_font(image):
    import numpy as np
    image = cv2.bitwise_not(image)
    kernel = np.ones((2, 2), np.uint8)
    image = cv2.erode(image, kernel, iterations=1)
    image = cv2.bitwise_not(image)
    return (image)


eroded_image = thin_font(no_noise)
cv2.imwrite("eroded_image.jpg", eroded_image)
#display("eroded_image.jpg")


def thick_font(image):
    import numpy as np
    image = cv2.bitwise_not(image)
    kernel = np.ones((2, 2), np.uint8)
    image = cv2.dilate(image, kernel, iterations=1)
    image = cv2.bitwise_not(image)
    return (image)


dilated_image = thick_font(no_noise)
cv2.imwrite("dilated_image.jpg", dilated_image)
#display("dilated_image.jpg")


# ROTATION AND DESKEWING------------------------------------------
new = cv2.imread("page_01_rotated.jpeg")

import numpy as np

def getSkewAngle(cvImage) -> float:
    # Prep image, copy, convert to gray scale, blur, and threshold
    newImage = cvImage.copy()
    gray = cv2.cvtColor(newImage, cv2.COLOR_BGR2GRAY)
    blur = cv2.GaussianBlur(gray, (9, 9), 0)
    thresh = cv2.threshold(blur, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)[1]

    # Apply dilate to merge text into meaningful lines/paragraphs.
    # Use larger kernel on X axis to merge characters into single line, cancelling out any spaces.
    # But use smaller kernel on Y axis to separate between different blocks of text
    kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (30, 5))
    dilate = cv2.dilate(thresh, kernel, iterations=2)

    # Find all contours
    contours, hierarchy = cv2.findContours(dilate, cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)
    contours = sorted(contours, key = cv2.contourArea, reverse = True)
    for c in contours:
        rect = cv2.boundingRect(c)
        x,y,w,h = rect
        cv2.rectangle(newImage,(x,y),(x+w,y+h),(0,255,0),2)

    # Find largest contour and surround in min area box
    largestContour = contours[0]
    print (len(contours))
    minAreaRect = cv2.minAreaRect(largestContour)
    cv2.imwrite("temp/boxes.jpg", newImage)
    # Determine the angle. Convert it to the value that was originally used to obtain skewed image
    angle = minAreaRect[-1]
    if angle < -45:
        angle = 90 + angle
    return -1.0 * angle
# Rotate the image around its center
def rotateImage(cvImage, angle: float):
    newImage = cvImage.copy()
    (h, w) = newImage.shape[:2]
    center = (w // 2, h // 2)
    M = cv2.getRotationMatrix2D(center, angle, 1.0)
    newImage = cv2.warpAffine(newImage, M, (w, h), flags=cv2.INTER_CUBIC, borderMode=cv2.BORDER_REPLICATE)
    return newImage

def deskew(cvImage):
    angle = getSkewAngle(cvImage)
    return rotateImage(cvImage, -1.0 * angle)

fixed = deskew(new)
cv2.imwrite("page_01_fixed.jpg", fixed)
#display("page_01_fixed.jpg")


# REMOVING BORDERS--------------------------
def remove_borders(image):
    contours, heiarchy = cv2.findContours(image, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    cntsSorted = sorted(contours, key=lambda x:cv2.contourArea(x))
    cnt = cntsSorted[-1]
    x, y, w, h = cv2.boundingRect(cnt)
    crop = image[y:y+h, x:x+w]
    return(crop)


no_borders = remove_borders(no_noise)
cv2.imwrite("no_borders.jpg", no_borders)
#display("no_borders.jpg")


# MISSING BORDERS----------------------------
color = [255, 255, 255]
top, bottom, left, right = [150] * 4
image_with_border = cv2.copyMakeBorder(no_borders, top, bottom, left, right, cv2.BORDER_CONSTANT, value=color)

cv2.imwrite("image_with_border.jpg", image_with_border)
#display("image_with_border.jpg")