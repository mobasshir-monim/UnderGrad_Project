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

# load the example image
image = cv2.imread("hasib1.jpg")
# pre-process the image by resizing it, converting it to
# graycale, blurring it, and computing an edge map
image = imutils.resize(image, height=500)
image = image[125 : image.shape[0] - 280, 270 : image.shape[1] - 290]
image = cv2.fastNlMeansDenoisingColored(image, None, 0, 300, 7, 21)
gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
# blurred = cv2.GaussianBlur(gray, (5, 5), 0)
edged = cv2.Canny(gray, 50, 200, 255)


# threshold the warped image, then apply a series of morphological
# operations to cleanup the thresholded image
thresh = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)[1]
kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (1, 5))
thresh = cv2.morphologyEx(thresh, cv2.MORPH_OPEN, kernel)
cv2.imshow("edged", thresh)
cv2.waitKey(0)
# cv2.imshow("edged", edged)
# cv2.waitKey(0)
# blurred = cv2.GaussianBlur(gray, (5, 5), 100)
# thresh = cv2.threshold(blurred, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)[1]
# kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (1, 5))
# thresh = cv2.morphologyEx(thresh, cv2.MORPH_OPEN, kernel)
# # find contours in the thresholded image, then initialize the
# # digit contours lists
# cnts = cv2.findContours(
#     thresh.copy(),
#     cv2.RETR_EXTERNAL,
#     cv2.CHAIN_APPROX_SIMPLE,
# )
# cnts = imutils.grab_contours(cnts)

# initCnts = []
# # loop over the digit area candidates
# for c in cnts:
#     # compute the bounding box of the contour
#     (x, y, w, h) = cv2.boundingRect(c)
#     # if the contour is sufficiently large, it must be a digit
#     # print(x, y, w, h)
#     if not (h >= 100 and h <= 250):
#         points = np.array(
#             [
#                 [x - 50, y - 50],
#                 [x + w + 50, y - 50],
#                 [x + w + 50, y + h + 50],
#                 [x - 50, y + h + 50],
#             ]
#         )
#         cv2.fillPoly(thresh, [points], 0)
#     else:
#         initCnts.append(c)

# digitCnts = []
# for c in initCnts:
#     points = np.column_stack(np.where(thresh.transpose() > 0))
#     # print(f"pts {points.shape}")
#     hull = cv2.convexHull(points)
#     # print(f"hull {hull.shape}")

#     # draw white filled hull polygon on black background
#     mask = np.zeros(thresh.shape, dtype=thresh.dtype)
#     # mask = np.zeros_like(roi)
#     cv2.fillPoly(mask, [hull], 255)
#     # cv2.imshow("mask", mask)
#     cv2.waitKey(0)
#     cnts = cv2.findContours(
#         mask,
#         cv2.RETR_EXTERNAL,
#         cv2.CHAIN_APPROX_SIMPLE,
#     )
#     cnt = imutils.grab_contours(cnts)[0]
#     (x, y, w, h) = cv2.boundingRect(cnt)
#     if w < 45:
#         cnt[0] = [[x - 175, y - 10]]
#         cnt[1] = [[x - 175, y + h + 15]]
#     digitCnts.append(cnt)
#     print(cnt)
# # sort the contours from left-to-right, then initialize the
# # actual digits themselves
# digitCnts = contours.sort_contours(digitCnts, method="left-to-right")[0]
# digits = []

# for c in digitCnts:
#     # extract the digit ROI
#     (x, y, w, h) = cv2.boundingRect(c)
#     # print(x, y, w, h)
#     roi = thresh[y : y + h, x : x + w]
#     # compute the width and height of each of the 7 segments
#     # we are going to examine
#     (roiH, roiW) = roi.shape
#     (dW, dH) = (int(roiW * 0.25), int(roiH * 0.15))
#     dHC = int(roiH * 0.05)
#     # define the set of 7 segments
#     segments = [
#         ((0, 0), (w, dH)),  # top
#         ((0, 0), (dW, h // 2)),  # top-left
#         ((w - dW, 0), (w, h // 2)),  # top-right
#         ((0, (h // 2) - dHC), (w, (h // 2) + dHC)),  # center
#         ((0, h // 2), (dW, h)),  # bottom-left
#         ((w - dW, h // 2), (w, h)),  # bottom-right
#         ((0, h - dH), (w, h)),  # bottom
#     ]
#     on = [0] * len(segments)
#     for i, ((xA, yA), (xB, yB)) in enumerate(segments):
#         # extract the segment ROI, count the total number of
#         # thresholded pixels in the segment, and then compute
#         # the area of the segment
#         segROI = roi[yA:yB, xA:xB]
#         total = cv2.countNonZero(segROI)
#         area = (xB - xA) * (yB - yA)
#         # if the total number of non-zero pixels is greater than
#         # 50% of the area, mark the segment as "on"
#         if float(area) > 0 and total / float(area) > 0.3:
#             on[i] = 1

#         cv2.rectangle(image, (x, y), (x + w, y + h), (255, 255, 255), 1)
#         print(tuple(on))
#         if tuple(on) in DIGITS_LOOKUP:
#             digit = DIGITS_LOOKUP[tuple(on)]
#             digits.append(digit)
#             cv2.putText(
#                 image,
#                 str(digit),
#                 (x - 10, y - 10),
#                 cv2.FONT_HERSHEY_SIMPLEX,
#                 0.65,
#                 (0, 255, 0),
#                 2,
#             )

# cv2.imshow("Processed Video", image)
# cv2.waitKey(0)
