import tkinter as tk

def main():
    window = tk.Tk()

    # gif is list, each frame an element in list, 5 frames in gif
    idle = [tk.PhotoImage(file='wisp.gif',format = 'gif -index %i' %(i)) for i in range(5)]
    
    frame_index = 0
    current_image = idle[frame_index]

    # changing window appearances/functionality
    window.overrideredirect(True) # make window frameless
    window.attributes('-topmost', True) # window on top
    window.wm_attributes('-transparentcolor', 'black') # turn black into transparency

    label = tk.Label(window, bd=0, bg='black') # bd=border size, bg=background
    label.configure(image=current_image) # add image to label
    label.pack() # make label appear on window

    x_pos = 0
    y_pos = 500

    window.geometry(f"64x64+{x_pos}+{y_pos}")
    
    window.mainloop()

if __name__ == '__main__':
    main()