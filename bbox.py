from PIL import Image
import os

###
# infile: output of CRAFT, *.txt file that contains bbox coordinates [x0,y0,x1,y1,x2,y2,x3,y3] 
# outfile: *_box.txt file that lists sorted bbox [line_id,block_id,xmin,ymin,xmax,ymax] 
# outfile2: *_line.txt file that lists segmented line bbox [line_id,block_id,xmin,ymin,xmax,ymax] 
###
def sort_bbox(infile):  
  folder = os.path.dirname(infile)
  filename, txt = os.path.splitext(os.path.basename(infile))  
  outfile = folder + '/' + filename + '_box' + txt     
  outfile2 = folder + '/' + filename + '_line' + txt      

  with open(infile, 'r', encoding='utf-8') as f:
    line = [' '.join(l.strip().split()) for l in f]   
  
  num_box = len(line)
  boxes = []
  lines = []
  py_ave = 0

  ## boxes contains minimum x, y coordinates of the bbox 
  for i, l in enumerate(line):
    xy = l.split(',')
    xmin = min(int(xy[0]), int(xy[6]))  
    xmax = max(int(xy[2]), int(xy[4]))
    ymin = min(int(xy[1]), int(xy[3]))
    ymax = max(int(xy[5]), int(xy[7]))
    py = ymax-ymin
    py_ave += py
    boxes.append([i, xmin, ymin, xmax, ymax])       
  # print(boxes)
    
  py_ave /= num_box
  print(f"average line height: {py_ave:.0f} pixels")
  thresh = py_ave/2
  
  ## sorted_box contains boxes sorted by y-coordinate, then x-coordinate
  sorted_box = sorted(boxes, key=lambda pair: (pair[2], pair[1]))
  # print(sorted_box)

  ## Group each line based on the half of box heights as threshold
  ymin_0 = sorted_box[0][2]
  # print(y0)
  for i in range(num_box):
    ymin = sorted_box[i][2]
    if( ymin - ymin_0 < thresh ):
      sorted_box[i][2] = ymin_0
    else:
      ymin_0 = ymin
  # print(sorted_box)

  ## sorted_box_final is sorted based on x coordinates of each line
  sorted_box_final = sorted(sorted_box, key=lambda pair: (pair[2], pair[1]))
  # print(sorted_box_final)

  ## Now print out the sorted bbox list as new boxfile
  line_id = 1
  block_id = 1
  index = sorted_box_final[0][0]  
  xmin_0 = sorted_box_final[0][1]
  ymin_0 = sorted_box_final[0][2]
  xmax_0 = sorted_box_final[0][3]
  ymax_0 = sorted_box_final[0][4]

  with open(outfile2, 'w', encoding='utf-8') as f2:
    with open(outfile, 'w', encoding='utf-8') as fo:
      for i in range(num_box):
        index = sorted_box_final[i][0]  
        xmin = sorted_box_final[i][1]
        ymin = sorted_box_final[i][2]
        xmax = sorted_box_final[i][3]
        ymax = sorted_box_final[i][4]
        if( ymin - ymin_0 > thresh ):
          f2.write("{},{},{},{},{},{}\n".format(line_id,block_id,xmin_0,ymin_0,xmax_0,ymax_0))  
          line_id += 1
          if( ymin - ymax_0 > thresh*2):
            block_id += 1
          ymin_0 = ymin
          ymax_0 = ymax 
          xmin_0 = xmin
          xmax_0 = xmax
        else:
          if(xmin - xmax_0 < thresh*2):
            if(ymax_0 < ymax):
              ymax_0 = ymax
            xmax_0 = xmax
          else:
            f2.write("{},{},{},{},{},{}\n".format(line_id,block_id,xmin_0,ymin_0,xmax_0,ymax_0))  
            ymin_0 = ymin
            ymax_0 = ymax 
            xmin_0 = xmin
            xmax_0 = xmax
        
        fo.write("{},{},{},{},{},{}\n".format(line_id,block_id,xmin,ymin,xmax,ymax))        
      f2.write("{},{},{},{},{},{}\n".format(line_id,block_id,xmin_0,ymin_0,xmax_0,ymax_0)) 

# sort_bbox('/home/jw/data/test/1/CRAFT/report.txt')

### 
# find all .txt files in the given directory and run sort_bbox(craftfile)
###
def sort_bbox_folder(directory):
  for file in os.listdir(directory):
    if file.endswith('.txt'):
      if not file.endswith('box.txt'):
        filepath = os.path.join(directory,file)
        print(filepath)
        sort_bbox(filepath)

# sort_bbox_folder('/home/jw/data/test/1/CRAFT')
   
###
# imfile: image file
# type: '_box' or '_line'
# boxfile: box file that is associated with the imfile
# output: /imagename/imagename_#.ext cropped images based on bbox boundaries
###
def extract_bbox(imfile,type): # post-process CRAFT to write text bbox images
    folder = os.path.dirname(imfile)
    imname, ext = os.path.splitext(os.path.basename(imfile))
    outpath = folder + '/' + imname + type + '/'
    boxfile = folder + '/CRAFT/' + imname + type + '.txt'
    # print(ext)
    # print(boxfile)
    try:
        os.makedirs(outpath)
    except:
        print("folder already exists")   

    im = Image.open(imfile)
    with open(boxfile, 'r', encoding='utf-8') as f:
        lines = [' '.join(l.strip().split()) for l in f]        
    f.close()
    num_box = len(lines)
    for i, l in enumerate(lines):
        xy = l.split(',')
        xmin = int(xy[2])
        xmax = int(xy[4])
        ymin = int(xy[3])
        ymax = int(xy[5])
 
        crop_box = (xmin, ymin, xmax, ymax)
        # print(crop_box)
        cropped_image = im.crop(crop_box)
        cropped_image_path = outpath + '/' + imname + '_' + f"{i+1:03}" + ext
        cropped_image.save(cropped_image_path)

# extract_bbox('/home/jw/data/test/1/report.png', '_box')

def extract_bbox_folder(directory):
    entries = os.listdir(directory)
    files = [entry for entry in entries if os.path.isfile(os.path.join(directory, entry))]
    for file in files:
        print(file)
        extract_bbox(directory+'/'+file, '_line')
        extract_bbox(directory+'/'+file, '_box')
        
# extract_bbox_folder('/home/jw/data/test/1/')
