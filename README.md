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
### tesseract 돌리기
```
tesseract /home/jw/data/ocrdata/test/메뉴1.jpg out -l eng+kor --tessdata-dir ./tessdata --oem 1 --psm 11

tesseract /home/jw/data/ocrdata/test/화장품/화장품_10.jpg out -l eng+kor --tessdata-dir ./tessdata  --oem 1 --psm 8
```
oem은 OCR engine mode로서 1(nerual nets) 또는 3(best available)을 선택한다. 
psm은 페이지 문단

