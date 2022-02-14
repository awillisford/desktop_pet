import tkinter as tk
import time
import pyautogui
from PIL import Image, ImageSequence, ImageTk, ImageOps # imageOps for mirror

class Pet():
    def __init__(self):
        self.time = time.time() # keep track of time between animation frames
        
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


        x_distance = x_mouse - self.x_pos
        y_distance = y_mouse - self.y_pos
        if abs(x_distance) >= abs(y_distance):
            large_to_small = abs(x_distance / y_distance) # ratio of x:y
        else:
            large_to_small = abs(y_distance / x_distance) # ratio of y:x
        self.window.geometry(f"{self.dim[0]}x{self.dim[1]}+{self.x_pos}+{self.y_pos}") 

        self.window.after(10, self.update)


if __name__ == '__main__':
    Pet()
    