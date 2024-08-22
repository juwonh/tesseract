# tesseract
### 설치
```
git clone https://github.com/juwonh/tesseract
cd tesseract
python3 -m venv venv
. venv/bin/activate

sudo apt install tessearct-ocr
sudo apt install libtesseract-dev
sudo apt install tesseract-ocr-kor
pip install pytesseract
pip install numpy
pip install opencv-python
```
### 이미지 bbox 제작 <bbox.py>
```
sort_bbox_folder('/home/jw/data/test/2/CRAFT') 돌린 후
extract_bbox_folder('/home/jw/data/test/2/') 돌림
```
### tesseract 돌리기 <test.py>
```
runTessWords(imfile, conf)
```
command line interface
```
한줄일 경우:
tesseract /home/jw/data/test/1/news_line/news_2.png out -l kor --tessdata-dir ./tessdata --psm 7

tesseract /home/jw/data/test/1/newsm_line/newsm_1.jpg out -l kor --tessdata-dir ./tessdata --psm 7

언어가 두 개 이상일 경우 정확도 떨어짐:
tesseract /home/jw/data/test/1/report_line/report_2.png out -l kor+eng --tessdata-dir ./tessdata --psm 7

한 단어일 경우
tesseract /home/jw/data/test/1/news_box/news_1.png out -l kor --tessdata-dir ./tessdata  --psm 8

tesseract /home/jw/data/test/1/report_box/report_4.png out -l kor+eng --tessdata-dir ./tessdata --psm 8

tesseract /home/jw/data/ocrdata/test/화장품/화장품_10.jpg out -l eng+kor --tessdata-dir ./tessdata  --oem 1 --psm 8
```
oem은 OCR engine mode로서 1(nerual nets) 또는 3(best available)을 선택한다. 
psm은 페이지 문단

