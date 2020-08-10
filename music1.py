from tkinter import *
from pygame import mixer
import tkinter.messagebox
from tkinter import filedialog
import os
from mutagen.mp3 import MP3
from tkinter import ttk
import time
import threading
from ttkthemes import ThemedTk
import webbrowser

Musicplaylist=[]
root= ThemedTk(theme="breeze")

# initializing mixer from pygame module . It's responsible for playing music
mixer.init()
# The initial window size
root.geometry('670x400')
root.title('Rustic MUSIC PLAYER')
root.iconbitmap('icon.ico')

def deletethesong():
    selected_to_delete=playlist.curselection()
    the_song_to_delete=int(selected_to_delete[0])
    playlist.delete(the_song_to_delete)
    Musicplaylist.pop(the_song_to_delete)
    print(Musicplaylist)
def about():
    tkinter.messagebox.showinfo('HOW TO USE ','FIRST CHOOSE A SONG \n THEN PLAY \n CHECK OUT YOUR SYSTEM VOLUMN ')
def browsemusic():
    global filename
    filename=filedialog.askopenfile()
    print(filename)
def showerror():
    tkinter.messagebox.showerror('Error message','Please Select a music \n From Add song -> Select song -> After adding to playlist Select the one you want to listen \n CHECK OUT YOUR SYSTEM VOLUMN ')
def callback(url):
    webbrowser.open_new(url)
# ----------------------- menubar ---------------------------
menubar=Menu(root)
root.config(menu=menubar)
subMenu=Menu(menubar,tearoff=0)
helpsubmenu=Menu(menubar,tearoff=0)
#menubar.add_cascade(label='Exit',menu=subMenu)
menubar.add_cascade(label='Help',menu=helpsubmenu)
subMenu.add_command(label='Open',command=browsemusic)
subMenu.add_command(label='Exit',command=root.destroy)
helpsubmenu.add_command(label='ABOUT',command=about)



#------------------------------add text------------------------------------
filenametext=Label(root,text='WELCOME',relief=SUNKEN)
filenametext.pack(side=TOP,fill=X,pady=10)

# ----------------------------- Github ------------------------------------
link1 = Label(root, text="Get Code", fg="blue", cursor="hand2")
link1.pack(side=BOTTOM,fill=X)
link1.bind("<Button-1>", lambda e: callback("https://github.com/49paunilay/Music-player-With-python"))
# ------------------------ Statusbar ------------------------------------------
status=Label(root,text='songname',relief=SUNKEN,anchor=W)
status.pack(side=BOTTOM,fill=X)


# ------------------------ Details  - Length of a song -----------------------------
def showsongdetails(music_name):
    filenametext['text'] = f'Playing : {os.path.basename(music_name.name)}'
    filedata=os.path.splitext(music_name.name)
    print(filedata)
    if filedata[1]=='.mp3':
        #print('Control at least here')
        #print(filename.name)
        audio=MP3(music_name.name)
        #print('If you see')
        #totallength=audio.info.length()
        totallength=audio.info.length
        #print(totallength)

    else:
        print('Command came here')
        l1=mixer.Sound(music_name.name)
        totallength=l1.get_length()
    mins,secs=divmod(totallength,60)
    mins=round(mins)
    secs=round(mins)
    lengthlabel['text']=f'Length -> {mins} : {secs} '
# --------------------------------------- Starting a new thread -----
    threadvar=threading.Thread(target=startcount,args=(totallength,))
    threadvar.start()
    
    
# -------------------------------------------current length song -------
def startcount(totallength):
    cur_time=0
    while cur_time<=totallength and mixer.music.get_busy():
        if paused:
            continue
        else:
            mins,secs=divmod(cur_time,60)
            print(str(mins) + ' ' + str(secs))
            mins=round(mins)
            secs=round(secs)
            currentlabel['text']=f'CURRENT TIME -> {mins} : {secs} '
            time.sleep(1)
            cur_time+=1

# ------------------------ play music ---------------------------------

def playmusic():
    global paused
    if paused:
        try:
            mixer.music.unpause()
            status['text'] = f'Playing : {os.path.basename(filename.name)}'
            paused=False
        except NameError:
            tkinter.messagebox.showwarning('No Music Selected','Have you selected any music?')
    else:
        try:
            stopmusic()
            time.sleep(1)
            selected_song=playlist.curselection()
            print(selected_song)
            updated_selected_song=int(selected_song[0])
            the_exact_music=Musicplaylist[updated_selected_song]
            print(the_exact_music)
            #loading the music file
            mixer.music.load(the_exact_music)
            #play the music
            mixer.music.play()
            status['text'] = f'Playing : {os.path.basename(the_exact_music.name)}'
            print('LOADED')
            showsongdetails(the_exact_music)
        except:
            showerror()
# ----------------------------- stop music -------------------------------
def stopmusic():
    
    mixer.music.stop()
    status['text'] = 'MUSIC STOPPED'
    print('STOPPED')
# ----------------------------- Set volumn -------------------------------
def volumeset(val):
    # mixer.music.set_volume takes argument which is having value 0 - 1
    volume=float(val)/100
    mixer.music.set_volume(volume)
# ----------------------------- pause---------------------------------------
paused=False
def pausemusic():
    global paused
    paused=True
    mixer.music.pause()
    status['text']= 'Paused'
# ------------------------------ Rewind ------------------------------------
def rewindmusic():
    try:
        playmusic()
        status['text']=f'Music Rewinded Playing : {os.path.basename(filename.name)}'
    except NameError:
        showerror()
    
# ------------------------------- mute my music -------------------------------
mute=False
def mutemusic():
    global mute
    if mute:
        mixer.music.set_volume(0.50)
        mutebtn.configure(image=volumnimg)
        scale.set(50)
        mute=False
        
    else:
        mixer.music.set_volume(0)
        mutebtn.configure(image=muteimg)
        scale.set(0)
        mute=True
# -------------------------------------- Add to playlist -------------------
def addtolist(filename):
    showname=os.path.basename(filename.name)
    index=0
    playlist.insert(index,showname)
    playlist.pack(fill=X,pady=3)
    Musicplaylist.insert(index,filename)
    print(Musicplaylist)
    index=index+1

def Add_song():
    global filename
    filename=filedialog.askopenfile()
    addtolist(filename)

# ------------------------------ Frames ----------------------------------
leftframe=Frame(root)
rightframe=Frame(root)
leftframe.pack(side=LEFT,padx=5)
rightframe.pack(side=RIGHT)
bottomframe=Frame(root)
bottomframe.pack(side=BOTTOM)

    

#-------------------------------Current ----------------------------
currentlabel=Label(rightframe,text='Current Time ',relief =GROOVE)
currentlabel.pack()
#-------------------------------- length ----------------------------------
lengthlabel=Label(rightframe,text='Length')
lengthlabel.pack(pady=10)


#---------------------- Playlist ------------------------------------------
playlist=Listbox(leftframe)
playlist.pack(fill=X,pady=3)
# ---------------------Buttons under playlist-----------------------------
Addbutton=ttk.Button(leftframe,text='Add Song',command=Add_song)
Addbutton.pack(side=LEFT,padx=2)
delete_button=ttk.Button(leftframe,text='DELETE Song',command=deletethesong)
delete_button.pack(side=RIGHT,padx=2)

#------------------------photo for play button-----------------------------
play_photo = PhotoImage(file='playb.png')
pause_photo=PhotoImage(file='pause.png')
# ---------------------- format for photo----------------------------------
#photolabel=Label(root,image=photo)
#photolabel.pack()
# --------------------------- Frame of middle switches --------------------
switchFrame=Frame(rightframe)
switchFrame.pack(padx=15,pady=15)

#------------------------adding clickable play button-----------------------
play_button=ttk.Button(switchFrame,image=play_photo,command=playmusic)
play_button.pack(side=LEFT,padx=5)
#------------------------pause button --------------------------------------

pause_button = ttk.Button(switchFrame,image=pause_photo,command=pausemusic)
pause_button.pack(side=LEFT,padx=5)
#------------------------adding clickable stop button------------------------
stopimg=PhotoImage(file='Stop.png')
stop_button=ttk.Button(switchFrame,image=stopimg,command=stopmusic)
stop_button.pack(side=LEFT,padx=5)
#------------------------- Rewind ------------------------------------------
rewimg=PhotoImage(file='rewind.png')
rewind=ttk.Button(switchFrame,image=rewimg,command=rewindmusic)
rewind.pack(side=LEFT,padx=5)
# ------------------------- Volumn------------------------------------------
framevol=Frame(rightframe)
muteimg=PhotoImage(file='mute.png')
volumnimg=PhotoImage(file='vol.png')
framevol.pack(padx=15,pady=15)
mutebtn=ttk.Button(framevol,image=volumnimg,command=mutemusic)
mutebtn.grid(row=2,column=0)
# ----------------------- volume control using Scale widget -------------------
scale=ttk.Scale(rightframe,from_=0,to=100,orient=HORIZONTAL,command=volumeset)
# default value of the scale 
scale.set(50)
mixer.music.set_volume(0.5)
scale.pack(fill=X)

# ------------------------ closemain as threading is applied so we have to explicitely tell to close the window after the cross button is clicked--
def closemain():
    stopmusic()
    root.destroy()

# ------------------------ Overriding the cross as threading is applied -------
root.protocol("WM_DELETE_WINDOW",closemain)
# ---------------------- mainloop ---------------------------------------------
root.mainloop() 