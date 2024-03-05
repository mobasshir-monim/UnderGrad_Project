# import the necessary packages
from imutils.perspective import four_point_transform
from imutils import contours
import imutils
import cv2
import time
import numpy as np

# define the dictionary of digit segments so we can identify
# each digit on the thermostat
DIGITS_LOOKUP = {
    (1, 1, 1, 0, 1, 1, 1): 0,
    (0, 0, 1, 0, 0, 1, 0): 1,
    (1, 0, 1, 1, 1, 1, 0): 2,
    (1, 0, 1, 1, 0, 1, 1): 3,
    (0, 1, 1, 1, 0, 1, 0): 4,
    (1, 1, 0, 1, 0, 1, 1): 5,
    (1, 1, 0, 1, 1, 1, 1): 6,
    (1, 0, 1, 0, 0, 1, 0): 7,
    (1, 1, 1, 1, 1, 1, 1): 8,
    (1, 1, 1, 1, 0, 1, 1): 9,
}

image = cv2.imread("hasib2.jpg")
image = imutils.resize(image, height=500)
image = imutils.rotate(image, angle=-1)
image = image[0 : image.shape[0] - 280, 270 : image.shape[1] - 290]
image = cv2.fastNlMeansDenoisingColored(image, None, 0, 300, 7, 21)
gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
blurred = cv2.GaussianBlur(gray, (5, 5), 0)
edged = cv2.Canny(gray, 50, 200, 255)


points = np.column_stack(np.where(edged.transpose() > 0))
# print(f"pts {points.shape}")
hull = cv2.convexHull(points)
# print(f"hull {hull.shape}")

# draw white filled hull polygon on black background
mask = np.zeros(edged.shape, dtype=edged.dtype)
# mask = np.zeros_like(roi)
cv2.fillPoly(mask, [hull], 255)
# cv2.imshow("mask", mask)
# cv2.waitKey(0)
cnts = cv2.findContours(
    mask,
    cv2.RETR_EXTERNAL,
    cv2.CHAIN_APPROX_SIMPLE,
)
cnt = imutils.grab_contours(cnts)[0]
peri = cv2.arcLength(cnt, True)
approx = cv2.approxPolyDP(cnt, 0.1 * peri, True)
(x, y, w, h) = cv2.boundingRect(approx)

warped = gray[y - 5 : y + h + 5, x - 5 : x + w + 5]
output = image[y - 5 : y + h + 5, x - 5 : x + w + 5]
# warped = four_point_transform(gray, approx.reshape(4, 2))
# output = four_point_transform(image, approx.reshape(4, 2))

thresh = cv2.threshold(warped, 0, 255, cv2.THRESH_BINARY_INV | cv2.THRESH_OTSU)[1]
kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (1, 5))
thresh = cv2.morphologyEx(thresh, cv2.MORPH_OPEN, kernel)

# loop over each of the digits
(w, h) = thresh.shape
for i in range(0, 3):
    # extract the digit ROI
    roi = thresh[y : y + (h / 3) * i, x : x + (w / 3) * i]
    # compute the width and height of each of the 7 segments
    # we are going to examine
    (roiH, roiW) = roi.shape
    (dW, dH) = (int(roiW * 0.25), int(roiH * 0.15))
    dHC = int(roiH * 0.05)
    # define the set of 7 segments
    segments = [
        ((0, 0), (w, dH)),  # top
        ((0, 0), (dW, h // 2)),  # top-left
        ((w - dW, 0), (w, h // 2)),  # top-right
        ((0, (h // 2) - dHC), (w, (h // 2) + dHC)),  # center
        ((0, h // 2), (dW, h)),  # bottom-left
        ((w - dW, h // 2), (w, h)),  # bottom-right
        ((0, h - dH), (w, h)),  # bottom
    ]
    on = [0] * len(segments)
