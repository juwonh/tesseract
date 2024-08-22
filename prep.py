from PIL import Image
import os
import cv2
import numpy as np

def prepColor(imfile):
  image = cv2.imread(imfile)
  gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
  thresh = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)[1]

  coords = np.column_stack(np.where(thresh > 0))
  angle = cv2.minAreaRect(coords)[-1]
  print(angle) 
  # cv2.imshow('test',gray)
  # cv2.waitKey(0)

prepColor('/home/jw/data/test/2/pill1.jpg')