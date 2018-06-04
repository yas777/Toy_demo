# from tkinter import *

# canvas_width = 300
# canvas_height =300

# master = Tk()

# canvas = Canvas(master, 
#            width=canvas_width, 
#            height=canvas_height)
# canvas.pack()




# mainloop()

# from tkinter import filedialog
# from tkinter import *
# import tkinter as tk

    

# def write_slogan():
#     print("Tkinter is easy to use!")
#     video = tkinter.Frame(root, bg='#000000')
# 	video.pack(side=tkinter.BOTTOM,anchor=tkinter.S,expand=tkinter.YES,fill=tkinter.BOTH)

# root = tk.Tk()
# frame = tk.Frame(root)
# frame.pack()

# canvas_width = 300
# canvas_height =300

# canvas = Canvas(root, 
#            width=canvas_width, 
#            height=canvas_height)
# canvas.pack()

# button = tk.Button(frame, 
#                    text="QUIT", 
#                    fg="red",
#                    command=quit)
# button.pack(side=tk.LEFT)
# slogan = tk.Button(frame,
#                    text="Hello",
#                    command=write_slogan)
# slogan.pack(side=tk.LEFT)

# root.mainloop()

# from tkinter import *

# canvas_width = 300
# canvas_height =300

# master = Tk()

# canvas = Canvas(master, 
#            width=canvas_width, 
#            height=canvas_height)
# canvas.pack()




# mainloop()

# from tkinter import filedialog
# from tkinter import *
# import tkinter as tk

    

# def write_slogan():
#     print("Tkinter is easy to use!")
#     video = tkinter.Frame(root, bg='#000000')
# 	video.pack(side=tkinter.BOTTOM,anchor=tkinter.S,expand=tkinter.YES,fill=tkinter.BOTH)

# root = tk.Tk()
# frame = tk.Frame(root)
# frame.pack()

# canvas_width = 300
# canvas_height =300

# canvas = Canvas(root, 
#            width=canvas_width, 
#            height=canvas_height)
# canvas.pack()

# button = tk.Button(frame, 
#                    text="QUIT", 
#                    fg="red",
#                    command=quit)
# button.pack(side=tk.LEFT)
# slogan = tk.Button(frame,
#                    text="Hello",
#                    command=write_slogan)
# slogan.pack(side=tk.LEFT)

# root.mainloop()

import os
import sys
import tkinter

import gi
gi.require_version('Gst', '1.0')
from gi.repository import Gst, GObject

def on_sync_message(bus, message, window_id):
        if not message.structure is None:
            if message.structure.get_name() == 'prepare-xwindow-id':
                image_sink = message.src
                image_sink.set_property('force-aspect-ratio', True)
                image_sink.set_xwindow_id(window_id)

GObject.threads_init()
Gst.init(None)

window = tkinter.Tk()
window.geometry('500x400')

video = tkinter.Frame(window, bg='#000000')
video.pack(side=tkinter.BOTTOM,anchor=tkinter.S,expand=tkinter.YES,fill=tkinter.BOTH)

window_id = video.winfo_id()

player = Gst.ElementFactory.make('playbin', 'player')
print(player)
# player.set_property('video-sink', None)
player.set_property('uri', '/home/yaswanth/casuality_of_eeg/jhbuild/v.mp4')
player.set_state(Gst.State.PLAYING)

bus = player.get_bus()
bus.add_signal_watch()
bus.enable_sync_message_emission()
bus.connect('sync-message::element', on_sync_message, window_id)

window.mainloop()

