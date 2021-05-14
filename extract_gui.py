# img_viewer.py

from typing import Sized
import PySimpleGUI as sg
import os.path
from PIL import Image
from PySimpleGUI.PySimpleGUI import Button, Submit
import pytesseract
pytesseract.pytesseract.tesseract_cmd = r'C:\\Program Files\\Tesseract-OCR\\tesseract.exe'
import pandas as pd
from shutil import copyfile

# First the window layout in 2 columns

file_list_column = [
    [
        sg.Text("Choose Image Folder"),
        sg.In(size=(25, 1), enable_events=True, key="-FOLDER-"),
        sg.FolderBrowse(),
        sg.Button(button_text=" Extract ",disabled=True,key="-EXTRACT DATA-"),
    ],
    [
        sg.Listbox(
            values=[], enable_events=True, size=(60, 10), key="-FILE LIST-"
        )
    ],
    [
        sg.Multiline(size=(60, 5), key='-OUTPUT TEXT-')
    ],
    [
        sg.Button(button_text=" EXIT ",key="Exit")
    ],
]

# For now will only show the name of the file that was chosen
image_viewer_column = [
    [sg.Text("Choose an image from list on left:")],
    [sg.Text(size=(40, 1), key="-TOUT-")],
    [sg.Image(key="-IMAGE-")],
]

# ----- Full layout -----
layout = [
    [
        sg.Column(file_list_column),
        sg.VSeperator(),
        sg.Column(image_viewer_column),
    ]
]

window = sg.Window("Medical Form Data extractor", layout)



def extract_data(filename):
    img = filename
    imge = Image.open(img)
    imgGray = imge.convert('L')

    mystring = pytesseract.image_to_string(imgGray)

    data = mystring
    df = pd.DataFrame([x.split(';') for x in data.split('\n')])

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
    #print(raw_result_df)
    return raw_result_df





# Run the Event Loop
while True:
    event, values = window.read()
    if event == "Exit" or event == sg.WIN_CLOSED:
        break
    # Folder name was filled in, make a list of files in the folder
    if event == "-FOLDER-":
        folder = values["-FOLDER-"]
        try:
            # Get list of files in folder
            file_list = os.listdir(folder)
        except:
            file_list = []

        fnames = [
            f
            for f in file_list
            if os.path.isfile(os.path.join(folder, f))
            and f.lower().endswith((".png", ".gif",".jpg"))
        ]
        window["-FILE LIST-"].update(fnames)
    elif event == "-FILE LIST-":  # A file was chosen from the listbox
        try:
            filename = os.path.join(values["-FOLDER-"], values["-FILE LIST-"][0])         

            filename = filename.replace("/","\\")
            filename = filename.replace("\\","\\")
            #print(filename)
            
            # new_path = copyfile(filename, temp)   
            # print(new_path)
            # new_path = os.listdir("temp")
            # sg.popup(new_path)

            window["-TOUT-"].update(filename)
            window["-IMAGE-"].update(filename = filename,  size = (500,400))
            
            window.FindElement("-EXTRACT DATA-").Update(disabled=False)
        except:
            pass
    
    if event == '-EXTRACT DATA-':
        try:
            output_df = extract_data(filename)
            window["-OUTPUT TEXT-"].update(output_df)
        except:
            pass

window.close()