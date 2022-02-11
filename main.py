import tkinter as tk
import time

class Pet():
    def __init__(self):
        self.window = tk.Tk()

        # gif is list, each frame an element in list, 5 frames in gif
        self.idle = [tk.PhotoImage(file='wisp.gif',format = 'gif -index %i' %(i)) for i in range(5)]
        
        self.frame_index = 0
        self.current_image = self.idle[self.frame_index]

        # changing window appearances/functionality
        self.window.overrideredirect(True) # make window frameless
        self.window.attributes('-topmost', True) # window on top
        self.window.wm_attributes('-transparentcolor', 'black') # turn black into transparency

        self.label = tk.Label(self.window, bd=0, bg='black') # bd=border size, bg=background
        self.label.configure(image=self.current_image) # add image to label
        self.label.pack() # make label appear on window

        self.x_pos = 715
        self.y_pos = 511

        self.window.geometry(f"24x36+{self.x_pos}+{self.y_pos}")
        
        # run update() 0ms after mainloop starts
        self.window.after(0, self.update)
        self.window.mainloop()
    
    def update(self):
        self.frame_index = (self.frame_index + 1) % 5 # 5 frames in idle, circle back to zero at end
        self.current_image = self.idle[self.frame_index]

        self.label.configure(image=self.current_image)
        self.label.pack()

        self.window.after(50, self.update)


if __name__ == '__main__':
    Pet()
