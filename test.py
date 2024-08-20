import pytesseract
import numpy as np
import cv2
import os

from PIL import Image


# config_tesseract = '--tessdata-dir ./tessdata --psm 7'
# img = cv2.imread('/home/jw/data/test/1/report_line/report_8.png')

def runTesseract(imfile, conf):
  img = cv2.imread(imfile)
  rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
  text = pytesseract.image_to_string(rgb, lang='kor+eng', config=conf )
  # print(text)
  return(text[:-2])

### entire text
# runTesseract('/home/jw/data/test/1/news.png', './out.txt', '--tessdata-dir ./tessdata --psm 3')
### one line
# runTesseract('/home/jw/data/test/1/report_line/report_2.png', './out.txt', '--tessdata-dir ./tessdata --psm 7')
### one word
# runTesseract('/home/jw/data/test/1/report_box/report_1.png', './out.txt', '--tessdata-dir ./tessdata --psm 8')

###
# directory에 있는 CRAFT bbox image들을 줄, 단락으로 나누어 runTesseract로 문자 추출한다
###
def runDirectory(directory):
  if(directory[-1] == '/'):
    directory = directory[:-1]
  folder = os.path.dirname(directory)
  name = os.path.basename(directory)
  boxfile = folder + '/CRAFT/' + name + '.txt'
  print(boxfile)

  with open(boxfile, 'r', encoding='utf-8') as f:
    lines = [' '.join(l.strip().split()) for l in f]        

  entries = os.listdir(directory)
  files = [entry for entry in entries if os.path.isfile(os.path.join(directory, entry))]
  files.sort()

  line0 = 1
  para0 = 1
  with open('./out.txt', 'w', encoding='utf-8') as fo:
    for i, l in enumerate(lines):
      xy = l.split(',')
      line = int(xy[0])
      para = int(xy[1])
      
      if(line > line0):
        fo.write("\n")
      if(para > para0):
        fo.write("\n")
      text = runTesseract(directory+'/'+files[i], '--tessdata-dir ./tessdata --psm 8')
      fo.write("{} ".format(text))

      line0 = line
      para0 = para

      
   
runDirectory('/home/jw/data/test/1/report_box/')

# from pytesseract import Output
def bounding_box(result, img, i, color = (255,100,0)):
  x = result['left'][i]
  y = result['top'][i]
  w = result['width'][i]
  h = result['height'][i]
  cv2.rectangle(img, (x,y), (x+w,y+h), color, 2)
  return x, y, img

### tesseract 의 bounding box는 퀄리티가 별로 좋지 않음
def testBoundingBox(imfile):
  img = cv2.imread(imfile)
  rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
 
  result = pytesseract.image_to_data(rgb, config=conf, lang='kor+eng', output_type=Output.DICT)
  
  min_confidence = 40
  for i in range(0, len(result['text'])):
    #print(i)
    confidence = int(result['conf'][i])
    if confidence > min_confidence:
      #print(confidence)
      x, y, img = bounding_box(result, img, i)
      #print(x,y)
      text = result['text'][i]
      cv2.putText(img, text, (x,y-10), cv2.FONT_HERSHEY_SIMPLEX, 1.1, (0,0,255))
  cv2.imshow('test',img)
  cv2.waitKey(0)

# testBoundingBox('/home/jw/data/test/1/news.png')