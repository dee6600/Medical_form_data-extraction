from PIL import Image
import pytesseract
pytesseract.pytesseract.tesseract_cmd = r'C:\\Program Files\\Tesseract-OCR\\tesseract.exe'
import pandas as pd

img = r'pdf-pages\0015.jpg'
imge = Image.open(img)
imgGray = imge.convert('L')

mystring = pytesseract.image_to_string(imgGray)
print(mystring)

data = mystring
df = pd.DataFrame([x.split(';') for x in data.split('\n')])
#print(df)


for index, row in df.iterrows():
    #print(index,row[0])

    text_string = row[0]
    #print(text_string)
    if "ICP-MS" in text_string:
        print(index)
        print(text_string)

