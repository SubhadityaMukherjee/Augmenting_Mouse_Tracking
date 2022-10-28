from random import random
from secrets import choice
from tkinter import N
import pandas as pd
import os
import pyautogui as pg
import PySimpleGUI as sg
from PIL import Image, ImageTk

# Handling the Data
file_name = "./data/data_map.csv"
image_directory = "/Users/eragon/Documents/CODE/Github/Augmenting_Mouse_Tracking/data/"
df = pd.read_csv(file_name)
df = df.sample(frac=1, random_state=1).reset_index()  # shuffle

name_of_query_column = ["sentence"]
names_of_option_image_columns = ["option1", "option2"]
for name in names_of_option_image_columns:
    df[name] = image_directory + df[name]

correct_response_column = "correct"
num_entries = len(df[name_of_query_column].values)

layout = [
    [
        sg.Text(
            "Which image do you prefer in the following?", key="-INIT-", visible=True
        )
    ],
    [sg.Text(key="-CHOICE-", visible=False)],
    [
        sg.Image(key="-IMAGE1-", visible=False),
    ],
    [
        sg.VSeparator(color=sg.DEFAULT_BACKGROUND_COLOR),
    ],
    # [
    #     sg.VSeparator(color=sg.DEFAULT_BACKGROUND_COLOR),
    # ],
    [sg.Image(key="-IMAGE2-", visible=False)],
    [sg.VSeparator(color=sg.DEFAULT_BACKGROUND_COLOR)],
    [
        sg.Button("Left Image", key="-OPTION1-", visible=False),
        sg.Button("Right Image", key="-OPTION2-", visible=False),
    ],
    [sg.Button("Start", key="st")],  # quit
    [sg.Button("Leave ):", key="OK")],  # quit
]


def load_image(path, window, key):
    try:
        image = Image.open(path)
        image.thumbnail((200, 200))
        photo_img = ImageTk.PhotoImage(image)
        window[key].update(data=photo_img)
    except:
        print(f"Unable to open {path}!")


question_no = 0
# Create the window
window = sg.Window("Mouse Tracking", layout, element_justification='c')

user_results_dict = {}

event, values = window.read()
# window['-CHOICE-'].update(df[name_of_query_column].values[question_no])
window["-INIT-"].update(visible=True)
window["st"].update(visible=True)
center_screen = (pg.size()[0]/2 , pg.size()[1])
if event == "st":

    # Create an event loop
    while True:
        event, values = window.read()
        pg.moveTo(center_screen)
        window["-INIT-"].update(visible=False)
        window["st"].update(visible=False)

        window["-CHOICE-"].update(visible=True)
        window["-IMAGE1-"].update(visible=True)
        window["-IMAGE2-"].update(visible=True)
        window["-OPTION1-"].update(visible=True)
        window["-OPTION2-"].update(visible=True)
        chosen_q = df[name_of_query_column].values[question_no][0]
        window["-CHOICE-"].update(chosen_q)
        # image = Image.open(f"./downloaded_cards/{file_name}.jpg") #I prefer /
        # window["myimg"].update(
        # data = ImageTk.PhotoImage(file_image)
        # ) #update the myimg key
        load_image(
            df[names_of_option_image_columns[0]].values[question_no], window, "-IMAGE1-"
        )
        load_image(
            df[names_of_option_image_columns[1]].values[question_no], window, "-IMAGE2-"
        )
        if event == "-OPTION1-":
            chosen = 1
        elif event == "-OPTION2-":
            chosen = 2

        try:
            user_results_dict[chosen_q] = {
                "correct_answer": df[correct_response_column].values[question_no],
                "chosen": chosen,
                "correct": df[correct_response_column].values[question_no] == chosen,
            }

            question_no += 1
        except:
            pass
        print(user_results_dict)
        if event == sg.WIN_CLOSED or event == "OK":
            break

window.close()
