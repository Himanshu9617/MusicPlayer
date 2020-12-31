import os
from tkinter import *
import tkinter.messagebox
from tkinter import filedialog
import time
from tkinter import ttk  #theme tkinter
from ttkthemes import themed_tk as tk
import threading
from pygame import mixer

root = tk.ThemedTk()
root.configure(bg='#FAAC77') 
root.get_themes()
root.set_theme("blue") 

statusbar = ttk.Label(root,text="Welcome to our music player",relief=SUNKEN,anchor=W,font='Times 15 italic')
statusbar.pack(side=BOTTOM,fill=X)
 
#create the menu bar
menubar = Menu(root)
root.config(menu=menubar)


# create the submenu
subMenu = Menu(menubar,tearoff=0)  # to remove -- line

favlist = []
# fav list it contains the full path+filename
#playlist it contains the filename
#fullpath +filname is required to play the music 

def browse():
    global filename_path
    filename_path=filedialog.askopenfilename()
    add_to_playlist(filename_path)

def add_to_playlist(filename):
    filename = os.path.basename(filename)  #only file name   
    index = 0
    playlist.insert(index,filename)
    favlist.insert(index,filename_path)
    index +=1
    
menubar.add_cascade(label="File",menu=subMenu)
subMenu.add_command(label="Open",command=browse)
subMenu.add_command(label="Exit",command=root.destroy)

def about_us():
    tkinter.messagebox.showinfo('About us','This music player is built using Tkinter by Himanshu Yadav')

subMenu = Menu(menubar,tearoff=0)  # to remove -- line
menubar.add_cascade(label="Help",menu=subMenu )
subMenu.add_command(label="About us",command=about_us)


mixer.init() #for initialization of mixer (to play music)

root.geometry('1050x400')
root.title("MyPlayer")
p1 = PhotoImage(file="music-notes.png")
root.iconphoto(False,p1)

filelabel = ttk.Label(root,text="Let's Make Some Noise",font='Times 15 italic') 
filelabel.pack(pady=10)

#leftframe contains  - the list box
#rightframe contains  - the top middle and bottom frames

leftframe = Frame(root)
leftframe.pack(side=LEFT,padx=30,pady=30)

playlist = Listbox(leftframe,fg="green2", selectforeground="cyan", selectbackground="gray", width=50,height=15)
playlist.pack() 

addbtn = ttk.Button(leftframe,text="+ADD",command=browse,width=25)
addbtn.pack(side=LEFT)

def del_song():
    selected_song = playlist.curselection()  #index of selctede song
    selected_song = int(selected_song[0])# convert index into int.
    playlist.delete(selected_song)
    favlist.pop(selected_song)
    


delbtn = ttk.Button(leftframe,text="-Del",command=del_song,width=25)
delbtn.pack(side=LEFT)

rightframe = Frame(root,height=25)
rightframe.place()
rightframe.pack(pady=30)


topframe = Frame(rightframe)
topframe.pack()




lengthlabel = Label(topframe,text="Total Length:--:--",font='Arial 12 bold',bg='#C9C9BD') 
lengthlabel.pack(pady=8)



currenttimelabel = Label(topframe,text="Current Time:--:--",relief=GROOVE,font='Arial 12 bold',bg='#C9C9BD') 
currenttimelabel.pack()





def show_details(play_music):
    a = mixer.Sound(play_music)
    total_length = a.get_length()

    
    mins,secs = divmod(total_length,60)
    mins = round(mins)
    secs = round(secs)
    timeformat = '{:02d}:{:02d}'.format(mins,secs)
    lengthlabel['text']="Total Length - "+timeformat

    t1 = threading.Thread(target=start_count,args=(total_length,))
    t1.start()

def start_count(t):
    global paused
    # tos top cur. time when to resume or stop
    current_time=0
    while current_time<=t and mixer.music.get_busy():
        if paused:
            continue
        else:
            mins,secs = divmod(current_time,60)
            mins = round(mins)
            secs = round(secs)
            timeformat = '{:02d}:{:02d}'.format(mins,secs)
            currenttimelabel['text']="Current Time - "+timeformat
            time.sleep(1)
            current_time+=1
        
   

def play_song():
    global paused
    
    if paused:
        mixer.music.unpause()
        statusbar['text']="Music Resumed"
        paused = FALSE
    else:
        try:
            stop_song()
            time.sleep(1)
            selected_song = playlist.curselection()  #index of selctede song
            selected_song = int(selected_song[0])# convert index into int.
            play_it = favlist[selected_song]
            mixer.music.load(play_it)
            mixer.music.play()
            statusbar['text']="Playing Music - "+os.path.basename(play_it)
            show_details(play_it)
        except:
            tkinter.messagebox.showerror('File Not Found','Nothing is selected')

            
    
        
        
def stop_song():
    mixer.music.stop()
    statusbar['text']="Music Stopped"

paused = FALSE
def pause_song():
    global paused
    paused = TRUE
    mixer.music.pause()
    statusbar['text']="Music Paused"

def next_song():
    nex = playlist.curselection()
    nex = nex[0]+1
    playlist.selection_clear(0,END)
    playlist.activate(nex)
    playlist.selection_set(nex,last=None)
    play_song()

def prev_song():
    prev = playlist.curselection()# this return a number(tuple)
    prev = prev[0]-1 # subtract 1 to move to the previous songs 

    playlist.selection_clear(0, END)
    playlist.activate(prev)
    playlist.selection_set(prev, last=None)
    play_song()
    

def set_vol(val):   # val is in string
    volume = float(val)/100
    mixer.music.set_volume(volume) # mixer takes value only from 0 to 1

def rewind_song():
    play_song()

muted = FALSE

def mute_song():
    global muted
    if muted:
        #unmute the music
        mixer.music.set_volume(0.7)
        volumebtn.configure(image=volumephoto)
        scale.set(70)
        muted = FALSE
    else:
        mixer.music.set_volume(0)
        volumebtn.configure(image=mutephoto)
        scale.set(0)
        muted = TRUE
  

middleframe = Frame(rightframe)
middleframe.pack(pady=30,padx=30)
    

prephoto = PhotoImage(file="pre.png")
prebtn = ttk.Button(middleframe,image = prephoto, command=prev_song)
prebtn.grid(row=0,column=0,padx=5)

playphoto = PhotoImage(file="play.png")
playbtn = ttk.Button(middleframe,image = playphoto, command=play_song)
playbtn.grid(row=0,column=1,padx=5)

stopphoto = PhotoImage(file="stop.png")
stopbtn = ttk.Button(middleframe,image = stopphoto, command=stop_song)
stopbtn.grid(row=0,column=2,padx=5)

pausephoto = PhotoImage(file="pause.png")
pausebtn = ttk.Button(middleframe,image = pausephoto, command=pause_song)
pausebtn.grid(row=0,column=3,padx=5)

nextphoto = PhotoImage(file="next.png")
nextbtn = ttk.Button(middleframe,image = nextphoto, command=next_song)
nextbtn.grid(row=0,column=4,padx=5)



bottomframe = Frame(rightframe)
bottomframe.pack(side='left',padx=32)

rewindphoto = PhotoImage(file="rewind.png")
rewindbtn = ttk.Button(bottomframe,image = rewindphoto, command=rewind_song)
rewindbtn.grid(row=0,column=0)

mutephoto = PhotoImage(file="mute.png")
volumephoto = PhotoImage(file="volume.png")
volumebtn = ttk.Button(bottomframe,image = volumephoto, command=mute_song)
volumebtn.grid(row=0,column=1)


scale = ttk.Scale(bottomframe,length=200,from_=0,to=100,orient= HORIZONTAL, command=set_vol)
scale.set(80)
mixer.music.set_volume(0.8)
scale.grid(row=0,column=2,padx=30)



def on_closing():
    tkinter.messagebox.showinfo("Warning","Are you want to close")
    stop_song();
    root.destroy()
    
    
root.protocol("WM_DELETE_WINDOW",on_closing)

root.mainloop()
