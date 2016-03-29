# Definition of the PhotoSlide class
# reads in a photo and then the photo slides from left to right across the canvas
# This one happen

import animation
import Tkinter as tk

class PhotoSlide(animation.AnimatedObject):
    
    # Read in an image file
    def __init__(self,canvas,filename,x,y):
        self.canvas = canvas
        self.photo = tk.PhotoImage(file = filename)
        self.phototag = self.canvas.create_image(x,y, image=self.photo)
        self.photo_width=self.photo.width()
        self.delta = 5
        
    def move(self):
        if self.delta > 0:
            x1, y1 = self.canvas.coords(self.phototag)
            if x1 >= self.canvas.winfo_width()-self.photo_width/2: # bounce back from R wall
                self.delta *= -1
            
        elif self.delta < 0:
            x1, y1 = self.canvas.coords(self.phototag)
            if x1 <= self.photo_width/2: # bounce back from L wall
                self.delta *= -1
           
        self.canvas.move(self.phototag,self.delta,0) # move up to ceiling