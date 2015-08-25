from PIL import ImageTk
from PIL import Image
from Tkinter import Tk, Label, Button
import random
                
class GeoGame(object):

    def __init__(self, master):
        self.master = master
        master.title("GeoGame")

        self.smallim = Image.open("800px-Whole_world_-_land_and_oceans_12000.jpg")
        self.im2 = ImageTk.PhotoImage(self.smallim)

        self.label = Label(image=self.im2)
        click = self.label.bind("<Button-1>", self.callback)
        self.label.pack()
        data = self.load_file()
        self.city = self.choose_city(data)
	x = [x.strip() for x in self.city.split(',')] 

        print self.city

    def callback(self, event):
        print "clicked at", event.x, event.y
        click = [event.x, event.y]
	return click

    def load_file(self):
        f = open('database.txt', 'r').readlines()
        data = []
        for line in f:
            data.append(line)
        #f.close()
        return data

    def choose_city(self, data):
        number = random.randint(0,1)
        return data[number]
    

root = Tk()
myGeoGame = GeoGame(root)
root.mainloop()
