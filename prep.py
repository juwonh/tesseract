from PIL import Image
import os
import cv2
import numpy as np
import pytesseract
import time

def prepColor(imfile):

  start_time = time.time()
  img = cv2.imread(imfile)
  gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
  cv2.imwrite('/home/jw/data/test/gum_.jpg',gray)

  # invert = 255 - gray
  value, bw = cv2.threshold(gray, 127, 255, cv2.THRESH_BINARY)
  # value, bw = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)
  black_pixels = np.sum(bw == 0)
  white_pixels = np.sum(bw == 255)
  print(black_pixels)
  print(white_pixels)

  # np.ones((3,3), np.uint8)
  # test = cv2.dilate(bw, np.ones((3,3), np.uint8))
  # test = gray
  
  end_time = time.time()
  duration = end_time - start_time  
  print(f"***Processing time: {duration:.3f} seconds")

  # print(text)
  # cv2.imshow('_',test)
  # cv2.waitKey(0)



 
  
prepColor('/home/jw/data/test/gum.jpg')
# prepColor('/home/jw/data/test/2/pill2/line/pill2_003.jpg')