from PIL import ImageTk
from PIL import Image
from Tkinter import Tk, Label, Button
import random
import math
                
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
        self.data = self.load_file()
        self.tot_score = 0
        self.gamesetup()

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

    def choose_city(self):
        citylen = len(self.data)
        number = random.randint(0,citylen-1) #maybe not -1
        return self.data[number]
    
    def gamesetup(self):
        self.city = self.choose_city()
        self.city = [x.strip() for x in self.city.split(',')]
        print "Your city to find is: " + self.city[1]
        self.score = 0


    def gameplay(self):
        self.tot_score += self.distance_score()
        print "total score = " + str(self.tot_score)
        if str(self.click[0]) == str(self.city[4]) and str(self.click[1]) == str(self.city[5]):
            self.gamesetup()
        else:
            self.gamesetup()

    def distance_score(self):
        xdist = int(self.click[0]) - int(self.city[4])
        ydist = int(self.click[1]) - int(self.city[5])
        dist = int(math.sqrt((xdist + ydist)**2))
        score = 30 - dist*2
        if score < 0:
            score = 0
        print "round score = " + str(score)
        return score
        

root = Tk()
myGeoGame = GeoGame(root)
root.mainloop()
