import tkinter as tk
import time
import pyautogui
from PIL import Image, ImageSequence, ImageTk

class Pet():
    def __init__(self):
        self.time = time.time() # keep track of time between animation frames
        self.window = tk.Tk()

        # changing window appearance
        self.window.overrideredirect(True) # make window frameless
        self.window.attributes('-topmost', True) # window on top
        self.window.wm_attributes('-transparentcolor', 'black') # turn black into transparency

        # load wisp gif
        self.dim = (48,72)
        gif_wisp_idle = Image.open('wisp.gif')

        # resize frames, and put in ImageTk object list
        self.wisp_idle = [ImageTk.PhotoImage(frame.resize(self.dim)) for frame in ImageSequence.Iterator(gif_wisp_idle)]

        self.wisp_idle_frame_ct = len(self.wisp_idle)
        self.wisp_idle_frame_index = 0

        self.label = tk.Label(self.window, bd=0, bg='black') # bd=border size, bg=background
        self.label.configure(image=self.wisp_idle[self.wisp_idle_frame_index]) # add image to label
        self.label.pack() # make label appear on window

        self.x_pos = 715
        self.y_pos = 511

        self.window.geometry(f"{self.dim[0]}x{self.dim[1]}+{self.x_pos}+{self.y_pos}")
        
        # run update() 0ms after mainloop starts
        self.window.after(0, self.update)
        self.window.mainloop()
    
    def update(self):
        current_time = time.time()
        if self.time + .05 <= current_time: # wait 50 ms between frames
            self.time = current_time
            self.wisp_idle_frame_index = (self.wisp_idle_frame_index + 1) % self.wisp_idle_frame_ct # cycle through frame numbers
            self.current_image = self.wisp_idle[self.wisp_idle_frame_index]
            self.label.configure(image=self.wisp_idle[self.wisp_idle_frame_index])

        self.x_pos, self.y_pos = pyautogui.position() # mouse position (x, y)
        self.window.geometry(f"{self.dim[0]}x{self.dim[1]}+{self.x_pos + 50}+{self.y_pos + 50}") # 50 to right and 50 px down from mouse

        self.window.after(10, self.update)


if __name__ == '__main__':
    Pet()
