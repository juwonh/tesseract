import pytesseract
import numpy as np
import cv2

config_tesseract = '--tessdata-dir ./tessdata'

img = cv2.imread('.//content/table_test.jpg')
cv2_imshow(img) # BGR -> RGB
rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
cv2_imshow(rgb)