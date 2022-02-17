import tkinter as tk
import time
import pyautogui
from PIL import Image, ImageSequence, ImageTk, ImageOps # imageOps for mirror
import os.path
import math

class Pet():
    def __init__(self):
        self.time = time.time() # keep track of time between animation frames
        self.mouse_pos = [0, 0] # for moving wisp in front of mouse direction
        self.distance_confidence = 15
        
        # initialize wisp properties
        self.dim = (48,72)
        self.x_pos = 0
        self.y_pos = 0
        self.speed = 20

        # changing window appearance
        self.window = tk.Tk() # initialize window
        self.test = '250x250'
        self.window.geometry(f"{self.test}+{self.x_pos}+{self.y_pos}") # change AxB later for particle following wisp!!!!!
        self.window.overrideredirect(True) # make window frameless
        self.window.attributes('-topmost', True) # window on top
        self.window.configure(bg='black')
        self.window.wm_attributes('-transparentcolor', 'black') # turn black into transparency

        # load wisp gifs
        gif_wisp_right = Image.open('assets/wispR.gif')
        gif_wisp_left = Image.open('assets/wispL.gif')
        self.wisp_right = [ImageTk.PhotoImage(frame.resize(self.dim)) for frame in ImageSequence.Iterator(gif_wisp_right)] # resize frames, and put in ImageTk object list
        self.wisp_left = [ImageTk.PhotoImage(frame.resize(self.dim)) for frame in ImageSequence.Iterator(gif_wisp_left)] # resize frames, and put in ImageTk object list
        self.max_frames = len(self.wisp_right) # calculate number of frames in gif for looping gif
        self.frame_index = 0 # current frame for display
        self.facing = self.wisp_left # direction wisp is facing, default left

        # create label widget for displaying gif
        self.label = tk.Label(self.window, bg='black') # label for displaying gif 
        self.label.configure(image=self.wisp_right[self.frame_index]) # add image to label
        self.label.place(relx=.5, rely=.5, anchor='center') # centers image
        
        # run update() 0ms after mainloop starts
        self.window.after(0, self.update)
        self.window.mainloop()
    
    def update(self):
        x_mouse, y_mouse = pyautogui.position() # mouse position (x, y)
        
        if x_mouse < self.mouse_pos[0]:
            self.mouse_pos[0] = x_mouse
            x_mouse -= self.window.winfo_width()
        if x_mouse > self.mouse_pos[0]:
            self.mouse_pos[0] = x_mouse
            x_mouse += self.window.winfo_width()

        if y_mouse < self.mouse_pos[1]:
            self.mouse_pos[1] = y_mouse
            y_mouse -= self.window.winfo_height()
        if y_mouse > self.mouse_pos[1]:
            self.mouse_pos[1] = y_mouse
            y_mouse += self.window.winfo_height()

        distance = [x_mouse - self.x_pos, y_mouse - self.y_pos]
        if abs(distance[0]) > self.distance_confidence or abs(distance[1]) > self.distance_confidence: # if x or y distance not 0, then wisp move
            magnitude = math.sqrt(distance[0]*distance[0] + distance[1]*distance[1])
            unit_distance = [elem/magnitude for elem in distance]

            # chooses which direction wisp faces
            if unit_distance[0] > 0:
                self.facing = self.wisp_right
            if unit_distance[0] < 0:
                self.facing = self.wisp_left

            self.x_pos += int(unit_distance[0] * self.speed)
            self.y_pos += int(unit_distance[1] * self.speed)
            self.window.geometry(f"{self.test}+{self.x_pos}+{self.y_pos}")


        # wait 50 ms to change frame
        current_time = time.time()
        if self.time + .05 <= current_time:
            self.time = current_time
            self.frame_index = (self.frame_index + 1) % self.max_frames # cycle through frames
            self.current_image = self.facing[self.frame_index]
            self.label.configure(image=self.current_image) # update window image

        self.window.after(10, self.update) # wait 10 ms 


if __name__ == '__main__':
    # create mirrored gif from base asset 'wispL.gif'
    if not os.path.isfile('assets/wispR.gif'):
        img = Image.open('assets/wispL.gif')
        img_mirror = [ImageOps.mirror(frame) for frame in ImageSequence.Iterator(img)]
        img_mirror[0].save("assets/wispR.gif", save_all=True, append_images=img_mirror[1:])
    
    Pet()
    