from PIL import Image
import pytesseract
pytesseract.pytesseract.tesseract_cmd = r'C:\\Program Files\\Tesseract-OCR\\tesseract.exe'

img = r'pdf-pages\0005.jpg'
imge = Image.open(img)
imgGray = imge.convert('L')
#data=pytesseract.image_to_data(imgGray)

#print(data)

mystring = pytesseract.image_to_string(imgGray)
print(mystring)

# pdf = pytesseract.image_to_pdf_or_hocr(imge, extension='pdf')
# with open('test.pdf', 'w+b') as f:
#     f.write(pdf) # pdf type is bytes by default

# xml = pytesseract.image_to_alto_xml(imge)

# print(xml)

# f =  open("myxmlfile.xml", "wb")
# f.write(xml)
# f.close()

# hocr = pytesseract.image_to_pdf_or_hocr(imge, extension='hocr')

# print(hocr)
# f =  open("myxmlfile.xml", "wb")
# f.write(hocr)
# f.close()