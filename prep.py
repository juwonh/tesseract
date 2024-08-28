from PIL import Image
import os
import cv2
import numpy as np
import pytesseract
import time

def toGray(imfile):
  folder = os.path.dirname(imfile)
  imname, ext = os.path.splitext(os.path.basename(imfile))  
  outfile = folder + '/' + imname + '_' + ext

  img = cv2.imread(imfile)
  gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
  cv2.imwrite(outfile,gray)

# toGray('/home/jw/data/test/2/pill2.jpg')

def prepInvert(folder):
  for file in os.listdir(folder):
    
    imname, ext = os.path.splitext(file)  
    imfile = folder + '/' + file
    outfile = folder + '/' + imname + 'i' + ext
    print(imfile)
    img = cv2.imread(imfile)
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    h = img.shape[0]
    w = img.shape[1]
    sum = 0
    count = 0
    for x in range (3):
      for y in range (3):
        pixel_value = gray[y, x]
        sum += pixel_value
        pixel_value = gray[y, w-1-x]
        sum += pixel_value
        pixel_value = gray[h-1-y, x]
        sum += pixel_value
        pixel_value = gray[h-1-y, w-1-x]
        sum += pixel_value
        count += 4
        
    average = sum/count
    print(f"Average Pixel value {average:.1f}")
    
    if average < 127:
      gray = 255 - gray
      cv2.imwrite(imfile,gray)
   
    # # value, bw = cv2.threshold(gray, 127, 255, cv2.THRESH_BINARY)
    # value, bw = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)
    # black_pixels = np.sum(bw == 0)
    # white_pixels = np.sum(bw == 255)
    # print(f"{imname} {black_pixels} vs {white_pixels}")
    # if (black_pixels > white_pixels):
    #   gray = 255 - gray
    #   cv2.imwrite(imfile,gray)    

# prepInvert('/home/jw/data/test/3/pill2_/box/')


def toBW(folder):
  for file in os.listdir(folder):    
    imname, ext = os.path.splitext(file)  
    imfile = folder + '/' + file
    img = cv2.imread(imfile)
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    value, bw = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)
    cv2.imwrite(imfile,bw)

# toBW('/home/jw/data/test/3/pill2_/box/')


def reduceNoise(folder):
  height = 120
  
  for file in os.listdir(folder):    
    imname, ext = os.path.splitext(file)  
    imfile = folder + '/' + file
    img = cv2.imread(imfile)
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    h = img.shape[0]
    w = img.shape[1]
    # if (h>height):
    #   ratio = 1
    #   gray = cv2.resize(gray, None, fx=ratio, fy=ratio, interpolation=cv2.INTER_CUBIC)
    
    new = cv2.erode(gray, np.ones((3,3), np.uint8))
    new = cv2.dilate(new, np.ones((3,3), np.uint8))
    cv2.imwrite(imfile,new)

reduceNoise('/home/jw/data/test/3/pill2_/box/')

def test():
  # np.ones((3,3), np.uint8)
  # test = cv2.dilate(bw, np.ones((3,3), np.uint8))
  # test = gray
    
  start_time = time.time()
  end_time = time.time()
  duration = end_time - start_time  
  print(f"***Processing time: {duration:.3f} seconds")

  # print(text)
  # cv2.imshow('_',test)
  # cv2.waitKey(0)



 
  

# prepColor('/home/jw/data/test/2/pill2/line/pill2_003.jpg')