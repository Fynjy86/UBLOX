import cv2
from pyrealsense2 import *
from object_detector import *

img = cv2.imread("123.jpg")

detector = HomogeneousBgDetector()
countours = detector.detect_objects(img)

print(countours)

for cnt in countours:
    # рисуем полигон
    cv2.polylines(img, [cnt], True, (255,0,0), 2)


cv2.imshow("Img", img)
cv2.waitKey(0)