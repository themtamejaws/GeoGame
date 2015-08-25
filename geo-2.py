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
	self.click = []
        self.label = Label(image=self.im2)
        click = self.label.bind("<Button-1>", self.callback)
        self.label.pack()
        data = self.load_file()
        self.gamesetup(data)

    def callback(self, event):
        print "clicked at", event.x, event.y
        self.click = [event.x, event.y]
        self.gameplay()

    def load_file(self):
        f = open('database.txt', 'r').readlines()
        data = []
        for line in f:
            data.append(line)
        #f.close()
        return data

    def choose_city(self, data):
        citylen = len(data)
        number = random.randint(0,0)#citylen-1) #maybe not -1
        return data[number]
    
    def gamesetup(self, data):
        self.city = self.choose_city(data)
	self.city = [x.strip() for x in self.city.split(',')]
        print self.city
	print "Your city to find is: " + self.city[1]

    def gameplay(self):
        print "well done for clicking on the screen!"
	print self.click[0], self.city[4]

	if str(self.click[0]) == str(self.city[4]) and str(self.click[1]) == str(self.city[5]):
	    print "success"
	else:
  	    print "you suck"

root = Tk()
myGeoGame = GeoGame(root)
root.mainloop()
