from tkinter import *
import pygame
from tkinter import filedialog
import time
from mutagen.mp3 import MP3 #finding total length
import tkinter.ttk as ttk


#creating a window
window = Tk()
window.title("MyMp3")
window.geometry("620x410")
window.configure(bg='chocolate1')
window.iconphoto(False, PhotoImage(file='icons/icon.png'))

pygame.mixer.init()

global files
files = ""
#methods used for controls

def saving_playlist(file):
    list_data = list_box.get(0,END)
    try:
        with open(file, "w", encoding="utf-8") as file:
            for d in list_data:
                file.write(d + "\n")
    except:
        file = filedialog.asksaveasfile(defaultextension = ".txt",mode="w")
        for d in list_data:
            file.write(d + "\n")
        
        
def load_playlist():
    file = filedialog.askopenfilename(initialdir='playlists/',title="Choose A Playlist", filetypes=(("Text Files","*.txt"),))
    global files
    files = file
    with open(file, "r", encoding="utf-8") as file:
        for f in file:
            list_box.insert(END, f.strip())

        
def add_song(): # add a single song in playlist
    song = filedialog.askopenfilename(initialdir='songs/',title="Choose A Song", filetypes=(("mp3 Files","*.mp3"),))
    list_box.insert(END, song)

def add_many_song(): # add multiple songs in playlist
    songs = filedialog.askopenfilenames(initialdir='songs/',title="Choose A Song", filetypes=(("mp3 Files","*.mp3"),))
    for song in songs:
        list_box.insert(END, song)

def delete_song():
    stop()
    list_box.delete(ANCHOR)# remove the selected song from play list
    

def delete_all_songs():
    stop()
    list_box.delete(0, END)# remove all songs from playlist
    

def stop():
    pygame.mixer.music.stop()
    statusbar.config(text='')
    slider.config(value=0)
    
def play():
    stop()
    song = list_box.get(ACTIVE)# method that loads the song and plays it
    pygame.mixer.music.load(song)
    pygame.mixer.music.play(loops=0)
    global paused
    paused=False
    
    song_dur()


global paused # global variable to store if song is paused or not
paused = False

def pause(is_paused): # method to pause and unpause
    global paused
    paused = is_paused

    if paused:
        pygame.mixer.music.unpause()
        paused = False
    else:
        pygame.mixer.music.pause()
        paused = True

def next_song():
    nex = list_box.curselection()# this return a number(tuple)
    nex = nex[0]+1 # add 1 to move to next song in list_box

    list_box.selection_clear(0, END)
    list_box.activate(nex)
    list_box.selection_set(nex, last=None)
    play()

def prev_song():
    prev = list_box.curselection()# this return a number(tuple)
    prev = prev[0]-1 # subtract 1 to move to the previous songs 

    list_box.selection_clear(0, END)
    list_box.activate(prev)
    list_box.selection_set(prev, last=None)
    play()

def song_dur():#method that updates the status bar
    current_time = int(pygame.mixer.music.get_pos()/1000)

    
    formated_current_time = time.strftime('%M:%S', time.gmtime(current_time))

    current_song = list_box.curselection()# this return a number(tuple)
    try:
        song = list_box.get(current_song)# get the song to find the duration
    
    
        song = MP3(song)
        global duration #making global so that it can be accessed in slider 
        duration = song.info.length
        formated_duration = time.strftime('%M:%S', time.gmtime(duration))

    
        current_time+=1# updating current time to cover up time diff between slider updation and actual time
        k=slider.get()
        if int(k)==int(duration):
            statusbar.config(text=f'{formated_duration} / {formated_duration}')
        elif paused:
            pass
        elif int(slider.get())==current_time:
            slider_length = int(duration)
            slider.config(to=slider_length, value=current_time)
        else:
            slider_length = int(duration)
            slider.config(to=slider_length, value=slider.get())

            formated_current_time = time.strftime('%M:%S', time.gmtime(int(slider.get())))
            statusbar.config(text=f'{formated_current_time} / {formated_duration}')
            next_time = int(slider.get())
            next_time+=1
            slider.config(value=next_time)

    except:
        pass
        
    
    statusbar.after(1000,song_dur)#updating timer after every second

def slide(x):

    song = list_box.get(ACTIVE)
    pygame.mixer.music.load(song)
    pygame.mixer.music.play(loops=0, start=int(slider.get()))


def volume(x):
    pygame.mixer.music.set_volume(vol_slider.get())


    current_vol = pygame.mixer.music.get_volume()
    current_vol = current_vol * 100

    if int(current_vol<10):
        vol_meter.config(image=vol0)
    elif int(current_vol)<25:
        vol_meter.config(image=vol1)
    elif int(current_vol)<40:
        vol_meter.config(image=vol2)
    elif int(current_vol)<55:
        vol_meter.config(image=vol3)
    elif int(current_vol)<65:
        vol_meter.config(image=vol4)
    elif int(current_vol)<75:
        vol_meter.config(image=vol5)
    elif int(current_vol)<85:
        vol_meter.config(image=vol6)
    elif int(current_vol)==100:
        vol_meter.config(image=vol7)
    

global vol0
global vol1
global vol2
global vol3
global vol4
global vol5
global vol6
global vol7

vol0 =  PhotoImage(file='icons/VOL0.png',)
vol1 =   PhotoImage(file='icons/VOL1.png')
vol2 =  PhotoImage(file='icons/VOL2.png')
vol3 = PhotoImage(file='icons/VOL3.png')
vol4 =  PhotoImage(file='icons/VOL4.png')
vol5 =   PhotoImage(file='icons/VOL5.png')
vol6 =  PhotoImage(file='icons/VOL6.png')
vol7 = PhotoImage(file='icons/VOL7.png')

master_frame = Frame(window, bg="DarkOrange3")
master_frame.pack(pady=20)

#list to conatin the song names
list_box = Listbox(master_frame, bg="black", fg="green2", selectforeground="cyan", selectbackground="gray", width=50)
list_box.grid(row=0,column=0)

volume_frame = LabelFrame(master_frame,text="Volume")
volume_frame.grid(row=0,column=1,padx=30)
 
#loading the icons for control buttons
prev_icon =  PhotoImage(file='icons/backB.png')
next_icon =   PhotoImage(file='icons/nextB.png')
play_icon =  PhotoImage(file='icons/playB.png')
pause_icon = PhotoImage(file='icons/pauseB.png')
stop_icon = PhotoImage(file='icons/stopB.png')

slider = ttk.Scale(master_frame, from_=0, to=100, orient=HORIZONTAL, value=0, command=slide, length=450)
slider.grid(row=1,column=0,pady=10)

vol_slider = ttk.Scale(volume_frame, from_=1, to=0, orient=VERTICAL, value=1, command=volume, length=135)
vol_slider.pack(pady=10)


# creating a frame to contain buttons
control_frame = Frame(master_frame)
control_frame.grid(row=2,column=0)

vol_meter = Label(master_frame, image=vol7)
vol_meter.grid(row=1,rowspan=2, column=1,padx=30,pady=10)

#creating play,pause,next and previous buttons
play_button = Button(control_frame, image=play_icon , borderwidth=0, command= play, height = 50, width = 50)
pause_button = Button(control_frame, image=pause_icon , borderwidth=0, command=lambda:pause(paused), height = 50, width = 50)
next_button = Button(control_frame, image=next_icon , borderwidth=0, command=next_song, height = 50, width = 50)
prev_button = Button(control_frame, image=prev_icon , borderwidth=0, command=prev_song, height = 50, width = 50)
stop_button = Button(control_frame, image=stop_icon , borderwidth=0, command=stop, height = 50, width = 50)

play_button.grid(row=0, column=0,padx=10,pady=20)
pause_button.grid(row=0, column=1, padx=10,pady=20)
next_button.grid(row=0, column=2, padx=10,pady=20)
prev_button.grid(row=0, column=3, padx=10,pady=20)
stop_button.grid(row=0, column=4, padx=10,pady=20)

#creating a menu
my_menu = Menu(window)
window.config(menu=my_menu)

file_menu = Menu(my_menu)
my_menu.add_cascade(label="File", menu=file_menu)
file_menu.add_command(label="Load Playlist",command=load_playlist)
file_menu.add_command(label="Save PlayList",command=lambda:saving_playlist(files))

add_song_menu = Menu(my_menu)
my_menu.add_cascade(label="Add Songs", menu=add_song_menu)
add_song_menu.add_command(label="Add a song",command=add_song)
add_song_menu.add_command(label="Add multiple songs",command=add_many_song)

delete_song_menu = Menu(my_menu)
my_menu.add_cascade(label="Delete Songs", menu=delete_song_menu)
delete_song_menu.add_command(label="Delete this song",command=delete_song)
delete_song_menu.add_command(label="Delete all songs",command=delete_all_songs)



statusbar = Label(window, text='', bd=1, relief=GROOVE, anchor=E)
statusbar.pack(fill=X, side=BOTTOM, ipady=2)



window.mainloop()
