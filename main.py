import tkinter as tk
import time
import pyautogui
from PIL import Image, ImageSequence, ImageTk, ImageOps # imageOps for mirror
import os.path
import math

class Pet():
    def __init__(self):
        self.time = time.time() # keep track of time between animation frames
        self.mouse_pos = None # for moving wisp in front of mouse direction
        
        # initialize wisp properties
        self.dim = (48,72)
        self.x_pos = 0
        self.y_pos = 0
        self.speed = 10 # in pixels per second

        # changing window appearance
        self.window = tk.Tk() # initialize window
        self.window.geometry(f"{self.dim[0]}x{self.dim[1]}+{self.x_pos}+{self.y_pos}") # change AxB later for particle following wisp!!!!!
        self.window.overrideredirect(True) # make window frameless
        self.window.attributes('-topmost', True) # window on top
        self.window.wm_attributes('-transparentcolor', 'black') # turn black into transparency

        # load wisp gifs
        gif_wisp_right = Image.open('assets/wispR.gif')
        gif_wisp_left = Image.open('assets/wispL.gif')
        self.wisp_right = [ImageTk.PhotoImage(frame.resize(self.dim)) for frame in ImageSequence.Iterator(gif_wisp_right)] # resize frames, and put in ImageTk object list
        self.wisp_left = [ImageTk.PhotoImage(frame.resize(self.dim)) for frame in ImageSequence.Iterator(gif_wisp_left)] # resize frames, and put in ImageTk object list
        self.max_frames = len(self.wisp_right) # calculate number of frames in gif for looping gif
        self.frame_index = 0 # current frame for display

        # create label widget for displaying gif
        self.label = tk.Label(self.window, bg='black') # label for displaying gif 
        self.label.configure(image=self.wisp_right[self.frame_index]) # add image to label
        self.label.pack() # make label appear on window
        
        # run update() 0ms after mainloop starts
        self.window.after(0, self.update)
        self.window.mainloop()
    
    def update(self):
        x_mouse, y_mouse = pyautogui.position() # mouse position (x, y)
        current_time = time.time()
    
        # wait 50 ms to change frame
        if self.time + .05 <= current_time:
            self.time = current_time
            self.frame_index = (self.frame_index + 1) % self.max_frames # cycle through frames

            # mouse to left of wisp
            if x_mouse < self.x_pos:
                self.current_image = self.wisp_left[self.frame_index]
            # mouse to right of wisp
            else:
                self.current_image = self.wisp_right[self.frame_index]

            self.label.configure(image=self.current_image) # update window image

        '''
            magnitude of vector give closest distance
            so --> sqrt(x^2 + y^2) = d

            x/magnitude -> x comp unit vector
            y/magnitude -> y comp unit vector
        '''
        distance = [x_mouse - self.x_pos, y_mouse - self.y_pos] # distance vector
        magnitude = math.sqrt(distance[0]*distance[0] + distance[1]*distance[1])
        distance = [elem/magnitude for elem in distance] # distance unit vector
        
        if distance[0] != 0:
            self.x_pos += distance[0] * self.speed
        if distance[1] != 0:
            self.y_pos += distance[1] * self.speed

        self.window.geometry(f"{self.dim[0]}x{self.dim[1]}+{int(self.x_pos)}+{int(self.y_pos)}") 

        self.window.after(10, self.update)


if __name__ == '__main__':
    # create mirrored gif from base asset 'wispL.gif'
    if not os.path.isfile('assets/wispR.gif'):
        img = Image.open('assets/wispL.gif')
        img_mirror = [ImageOps.mirror(frame) for frame in ImageSequence.Iterator(img)]
        img_mirror[0].save("assets/wispR.gif", save_all=True, append_images=img_mirror[1:])
    
    Pet()
    