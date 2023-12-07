import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
from tkinter import Menu

import tensorflow as tf
from tensorflow import keras
import cv2
import numpy as np

import re # regex

from pytube import YouTube # download video

import os # delete video

import pymysql # for Database

import requests
from bs4 import BeautifulSoup # for youtube video title

import database_utils # module!

# db connection
db_connection = database_utils.connect_to_database('localhost', 'root', 'root', 'pbl4')


# working directory
wd = "/home/myeongseo/Desktop/PBL4/"


# select all checkbutton(categories)
def select_all(check_vars, all_var, update_func=None):
    if all_var.get() == 1:
        for var in check_vars:
            var.set(1)
    else:
        for var in check_vars:
            var.set(0)

    if update_func:
        update_func()

        	
# check button method
def checkbutton_status(check_vars, all_var):
    if (all_var == chk6):
        defaultBG = tk.Label().cget('background')
        result_label.config(text="result will be displayed here", bg = defaultBG, fg = '#000000')
        result_label.pack(fill="both")
    
    # check all cb checked
    selected_count = sum(var.get() for var in check_vars[:-1])
    total_count = len(check_vars) - 1  # exclude 'Select All'

    all_var.set(1 if selected_count == total_count else 0)


	
# check url, if it is youtube or not       	
def is_youtube():
    flag = False
    result = None
    
    URL = str(entry_url.get())
    
    youtube_regex = (
    	r'(http:|https?://)?(www\.)?'
        '(youtube|youtu|youtube-nocookie)\.(com|be)/'
        '(watch\?v=|embed/|v/|.+\?v=)?([^&=%\?]{11})'
    )
    
    youtube_shorts_regex = (
        r'(https?://)?(www\.)?'
        'youtu(be\.com|\.be)/'
        '(shorts/)?'
        '([^&=%\?]{11})'
    ) 

    
    match = re.match(youtube_shorts_regex, URL)
    
    if match :
        flag = True

    return flag


# get video id & title
def get_video_info(URL):
    # get video id
    v_id = None
    youtube_regex = (
        r'(https?://)?(www\.)?'
        'youtu(be\.com|\.be)/'
        '(shorts/)?'
        '([^&=%\?]{11})'
    )
    matches = re.search(youtube_regex, URL)
    if matches:
        v_id = matches.group(5) 
    
    # get video title
    r = requests.get(URL)
    soup = BeautifulSoup(r.text, features="html5lib")

    link = soup.find_all(name="title")[0]
    title = str(link)
    title = title.replace("<title>","")
    title = title.replace("</title>","")
    title = title.replace(" - YouTube","")      
    
    return v_id, title


# load ML model
def load_fire_model() :
    fire_model = tf.keras.models.load_model(wd + "flame/RealFireModel")
    return fire_model
   
def load_flooding_model() :
    flooding_model = tf.keras.models.load_model(wd + "flooding/flooding_model")
    return flooding_model

def load_violence_model() :
    pass

def load_carCrash_model() :
    carCrash_model = tf.keras.models.load_model(wd + "CarCrash/TrafficModel.h5")
    return carCrash_model


# download youtube video from URL to Local
def video_download(URL):
    # YouTube object
    yt = YouTube(URL)

    # best ghkwlf
    video_stream = yt.streams.get_highest_resolution()

    # set directory path and file name
    download_path = wd + "test"
    file_name = "test_video.mp4"  

    # download video
    video_stream.download(output_path=download_path, filename=file_name)


# test video, and return results
def model_predict(model, cat):
    print(wd)
    
    video_path = wd + "test/test_video.mp4"
    #video_path = wd + "test/fire1.mp4" # for test
    #video_path = wd + "test/flooding1.mp4" 
    #video_path = wd + "test/carCrash1.mp4"
    #video_path = "/media/sf_virtualbox_share/modelTest_video/carCrash/1.pm4"
    
    cap = cv2.VideoCapture(video_path)
    
    total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    max_consecutive_detections = 0
    current_streak = 0

    frame_interval = 5
    frame_counter = 0
    
    while True:
        ret, frame = cap.read()
        if not ret:
            break

        frame_counter += 1
        if frame_counter % frame_interval == 1:
            if cat == 'carCrash' :
                frame = cv2.resize(frame, (224, 224))
            else :
                frame = cv2.resize(frame, (32, 32))
            frame = np.expand_dims(frame, axis=0)
            predictions = model.predict(frame)

            if predictions[0][0] > 0.5:
                current_streak += 1
                max_consecutive_detections = max(max_consecutive_detections, current_streak)
            else:
                current_streak = 0 # reset counter

            print(f"Frame Class: {'Class 1' if predictions[0][0] > 0.5 else 'Class 0'}")

        if frame_counter == frame_interval:
            frame_counter = 0

    cap.release()
    
    print("Max consecutive class 1 frames:", max_consecutive_detections)
    print("Total frames:", total_frames)
    
    ten_percent = total_frames / 5 / 100 * 10
    return max_consecutive_detections >= ten_percent



# test button method
def test_func():
    result_label.config(text="checking . . .")
    result_label.pack(fill="both")
    
    unchecked = 0

    if not is_youtube():
        messagebox.showwarning("Warning", "Please enter the Youtube Shorts URL")
        result_label.config(text="result will be displayed here")
        return
        
    for var in checkbox_vars[:-1]:
        if var.get() == 0:
            unchecked += 1
    
    if unchecked == 4 : # if user didn't check any categories
        msg = "Please check the category"
        messagebox.showwarning("Warning",msg)
    else :  
        URL = str(entry_url.get())
        video_download(URL)  ############### download video

        category_tags = {'fire': 'FI', 'flooding': 'FL', 'violence': 'VI', 'carCrash': 'CC'}
        category_models = {'fire': load_fire_model, 'flooding': load_flooding_model, 'carCrash': load_carCrash_model,}
        #'violence': load_violence_model,
        results = []
     
        for cat, var in zip(category_tags.keys(), checkbox_vars[:-1]):
            if var.get() == 0:
                continue

            tag = category_tags[cat]
            if database_utils.search_in_db(db_connection, URL, tag):
                results.append(cat)
            elif cat in category_models:
                model_loader = category_models[cat]
                loaded_model = model_loader()
                if model_predict(loaded_model, cat):
                    results.append(cat)
                    database_utils.insert_into_db(db_connection, URL, tag) ### insert into DB
                 
        os.system("rm " + wd + "test/test_video.mp4") # remove video
    
    
        # print result
    
        if not results:
            set_text = "This video does not contain any of the selected categories"
            result_label.config(text=set_text, bg="light sky blue", fg="snow")
        else:
            set_text = "This Video contains: " + ", ".join(results)
            result_label.config(text=set_text, bg="magenta", fg="snow")

        result_label.pack(fill="both")
    
def del_entry():
    entry_url.delete(0, 'end')

def func_restart():
    func_exit()
    os.system("python3 ~/Desktop/PBL4/demo3_utils.py")
    
def func_exit():
    window.quit()
    window.destroy()



####### Make Window ####### 
window= tk.Tk()
window.title("demo ver.3")
window.geometry("1000x400")
window.resizable(True, True)

style = ttk.Style()
style.configure('Custom.TLabelframe', padding=(30,30))


####### make menu ####### 
mainMenu = tk.Menu(window)
window.config(menu = mainMenu)
m = Menu(mainMenu)
mainMenu.add_cascade(label="menu", menu=m)
m.add_command(label="restart", command=func_restart)
m.add_separator()
m.add_command(label="exit", command=func_exit)


####### make tab ####### 
notebook = ttk.Notebook(window)
notebook.pack(fill="both")

tab1 = ttk.Frame(window)
notebook.add(tab1, text='Tab 1')



####### Choose Category Label ####### 
label_frame = ttk.LabelFrame(tab1, text="Choose Category", style='Custom.TLabelframe')  
#style = 'Custom.TLabelframe'
label_frame.pack(fill="both")


# CheckButton Label for two lines
cb_label1 = tk.Label(label_frame)
cb_label1.pack(side="top")
    
cb_label2 = tk.Label(label_frame)
cb_label2.pack(side="top")


# make Checkbuttons
checkbox_vars = []

chk1 = tk.IntVar()
checkbox_vars.append(chk1)
cb_fire = tk.Checkbutton(cb_label1, variable=chk1, text="Fire", command=lambda:checkbutton_status(checkbox_vars, chk6))
    
chk2 = tk.IntVar()
checkbox_vars.append(chk2)
cb_flooding = tk.Checkbutton(cb_label1, variable=chk2, text="Flooding", command=lambda:checkbutton_status(checkbox_vars, chk6))
    
chk3 = tk.IntVar()
checkbox_vars.append(chk3)
cb_violence = tk.Checkbutton(cb_label1, variable=chk3, text="Violence", command=lambda:checkbutton_status(checkbox_vars, chk6))
   
chk4 = tk.IntVar()
checkbox_vars.append(chk4)
cb_carcrash = tk.Checkbutton(cb_label2, variable=chk4, text="Car Crash", command=lambda:checkbutton_status(checkbox_vars, chk6))

chk6 = tk.IntVar()
checkbox_vars.append(chk6)
cb_all = tk.Checkbutton(cb_label2, variable=chk6, text="Select All", command=lambda: select_all(checkbox_vars, chk6))


cb_fire.pack(side="left")
cb_flooding.pack(side="left")
cb_violence.pack(side="left")
cb_carcrash.pack(side="left")
cb_all.pack(side="left")


####### Test URL Input Label ####### 
test_label = tk.Label(tab1)
test_label.pack(padx=30, pady=30)
entry_url = tk.Entry(test_label, width = 80)
entry_url.pack(side="left", padx=10)

btn_del = tk.Button(test_label, text = "delete", command=del_entry)
btn_del.pack(side="right", padx=5)
    
btn_check = tk.Button(test_label, text = "check", command=test_func)
btn_check.pack(side="right")




####### Show Test Result Label ####### 
result = "result will be displayed here"
result_label = tk.Label(tab1, text=result, width = 20, height = 5)
result_label.pack(fill="both")





###########################
# code below is for tab 2 #
###########################

tab2 = ttk.Frame(window)
notebook.add(tab2, text='Tab 2')

firebtn_var = tk.IntVar()
floodbtn_var = tk.IntVar()
violencebtn_var = tk.IntVar()
carcrashbtn_var = tk.IntVar()
selectAll_var = tk.IntVar()

def init_treeview(parent):
    treeview = ttk.Treeview(parent, columns=["1", "2", "3", "4"], displaycolumns=["1", "2", "3", "4"])
    treeview.heading("#0", text="num")
    treeview.column("#0", anchor="center", width=50)
    treeview.heading("#1", text="title")
    treeview.column("#1", width=600)
    treeview.heading("#2", text="vid")
    treeview.column("#2", width=100)
    treeview.heading("#3", text="category")
    treeview.column("#3", anchor="center", width=70)

    return treeview


def update_treeview():
    global treeview
    
    # make connection for DB
    cursor = db_connection.cursor()
    
    treeview.delete(*treeview.get_children())
    
    if firebtn_var.get() == 1:
        sql = "select * from videos where category='FI'"
        cursor.execute(sql)
        results = cursor.fetchall()
        
        for row in results:
            treeview.insert('', 'end', text=row[0], values=[row[1], row[2], row[3]])
    
    if floodbtn_var.get() == 1:
        sql = "select * from videos where category='FL'"
        cursor.execute(sql)
        results = cursor.fetchall()
        
        for row in results:
            treeview.insert('', 'end', text=row[0], values=[row[1], row[2], row[3]])
        
    if violencebtn_var.get() == 1:
        sql = "select * from videos where category='VI'"
        cursor.execute(sql)
        results = cursor.fetchall()
        
        for row in results:
            treeview.insert('', 'end', text=row[0], values=[row[1], row[2], row[3]])
        
    if carcrashbtn_var.get() == 1:
        sql = "select * from videos where category='CC'"
        cursor.execute(sql)
        results = cursor.fetchall()
        
        for row in results:
            treeview.insert('', 'end', text=row[0], values=[row[1], row[2], row[3]])
        
        
    treeview.pack(fill="both", expand=True)
    
    cursor.close()
    
    checkbutton_status(tab2_cb_vars, selectAll_var)


#treeview
treeview = init_treeview(tab2)

#tab2_checkbutton
tab2_label_frame = ttk.LabelFrame(tab2, text="Choose Category")    
tab2_label_frame.pack(fill="both")

tab2_cb_label1 = tk.Label(tab2_label_frame)
tab2_cb_label1.pack(side="top")

tab2_cb_label2 = tk.Label(tab2_label_frame)
tab2_cb_label2.pack(side="top")

tab2_cb_vars = []

firebtn = tk.Checkbutton(tab2_cb_label1, text="fire", variable=firebtn_var, command=update_treeview)

floodbtn = tk.Checkbutton(tab2_cb_label1, text="flood", variable=floodbtn_var, command=update_treeview)

violencebtn = tk.Checkbutton(tab2_cb_label1, text="violence", variable=violencebtn_var, command=update_treeview)

carcrashbtn = tk.Checkbutton(tab2_cb_label2, text="carcrash", variable=carcrashbtn_var, command=update_treeview)

selectAllbtn = tk.Checkbutton(tab2_cb_label2, text="Select All", variable=selectAll_var, command=lambda: select_all(tab2_cb_vars, selectAll_var, update_treeview))

tab2_cb_vars.append(firebtn_var)
tab2_cb_vars.append(floodbtn_var)
tab2_cb_vars.append(violencebtn_var)
tab2_cb_vars.append(carcrashbtn_var)
tab2_cb_vars.append(selectAll_var)


# pack
firebtn.pack(side='left')
floodbtn.pack(side='left')
violencebtn.pack(side='left')
carcrashbtn.pack(side='left')
selectAllbtn.pack(side='left')

treeview.pack(fill="both", expand=True)

window.mainloop()


# 2023-12-07
