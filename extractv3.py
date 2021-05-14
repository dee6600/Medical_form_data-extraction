from PIL import Image
import pytesseract
pytesseract.pytesseract.tesseract_cmd = r'C:\\Program Files\\Tesseract-OCR\\tesseract.exe'
import pandas as pd

img = r'pdf-pages\0010.jpg'
imge = Image.open(img)
imgGray = imge.convert('L')

mystring = pytesseract.image_to_string(imgGray)
#print(mystring)

data = mystring
df = pd.DataFrame([x.split(';') for x in data.split('\n')])
#print(df)

with open("Technology_list.txt", "r") as Technology_list:
	lines = Technology_list.readlines()
T_list = [x.replace('\n', '') for x in lines]
#print(T_list)

with open("test_name_list.txt", "r") as test_name_list:
	lines = test_name_list.readlines()
TN_list = [x.replace('\n', '') for x in lines]
#print(TN_list)

keywords = T_list + TN_list

# print(keywords)

raw_result = []
for index, row in df.iterrows():
    #print(index,row[0])

    text_string = row[0]
    #print(text_string)
    for keyword in keywords:
        if keyword in text_string:
            # print(index)
            # print(text_string)
            raw_result.append(text_string)
            if keyword in TN_list:
                print("Test Name Match:",keyword)  
            elif keyword in T_list:
                print("Technology match:",keyword)
              

#print(raw_result)

with open("methods.txt", "r") as methods_list:
	lines = methods_list.readlines()
method_list = [x.replace('\n', '') for x in lines]

for method in method_list:
    while method in raw_result: raw_result.remove(method)  

#print(raw_result)

raw_result_df = pd.DataFrame(raw_result)
print(raw_result_df)