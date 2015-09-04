from PIL import ImageTk
from PIL import Image
from Tkinter import Tk, Label, Button, Frame, Text, END, DISABLED, RIGHT, TOP, BOTTOM, LEFT, Canvas
import tkFont
import random
import math
                
class GeoGame(Frame):

    def __init__(self, master):
        self.master = master
        master.title("GeoGame")
	
        self.smallim = Image.open("mediummap.jpg")
        self.bigim = Image.open("half.jpg")
	self.bigim.load()
	self.customFont = tkFont.Font(family="Comic Sans MS", size=12)
        self.im2 = ImageTk.PhotoImage(self.smallim)

	self.click = []


        self.topFrame = Frame(master)
        self.topFrame.pack(side=TOP)
        self.bottomFrame = Frame(master)
        self.bottomFrame.pack(side=BOTTOM, fill="both")
        self.canvas = Canvas(self.topFrame, width = 1200, height=600)
        self.canvas.pack(expand="yes", fill="both")
        self.label = self.canvas.create_image(0,0, image=self.im2, anchor='nw')
        click = self.canvas.bind("<Button-1>", self.callback)

        self.crosshairs = Image.open("smallcrosshair.gif") #GIFs ONLY, PNG's transparency doesn't work
        self.cross_width, self.cross_height = self.crosshairs.size
        self.cross = ImageTk.PhotoImage(self.crosshairs)
        self.first_round = 0
	self.zoomed = False        

        self.text = Text(self.bottomFrame, height=1, width=40, font=self.customFont)
        self.text.pack(side=LEFT)
        self.scoreText = Text(self.bottomFrame, height=1,width=10)
        self.scoreText.pack(side=RIGHT)
        self.scoreLabel = Label(self.bottomFrame, text="Score")
        self.scoreLabel.pack(side=RIGHT)
        self.text.insert(END, "Your next city is: ")
        self.text.config(state=DISABLED)
        self.data = self.load_file()
        self.tot_score = 0
        self.gamesetup()

    def change_to_big(self):
	self.canvas.delete(self.label)
	upper = (self.click[1]*10) - 300
	left = (self.click[0]*10) - 600
	right = (self.click[0]*10) + 600
	lower = (self.click[1]*10) + 300
	self.crop_big = self.bigim.crop((left, upper, right, lower))
	self.crop_big2 = ImageTk.PhotoImage(self.crop_big)
	self.zoom = self.canvas.create_image(0, 0, image=self.crop_big2, anchor='nw')
	self.zoomed = True	

    def change_to_small(self):
	self.canvas.delete(self.zoom)
	self.label = self.canvas.create_image(0,0, image=self.im2, anchor='nw')	
    	self.zoomed = False

    def callback(self, event):
        print "clicked at", event.x, event.y
        self.click = [event.x, event.y]
	if self.zoomed == False:
		self.change_to_big()
        else:
		self.gameplay()

    def load_file(self):
        f = open('sorted.txt', 'r').readlines()
        data = []
        for line in f:
            data.append(line)
        return data

    def choose_city(self):
        citylen = len(self.data)
        number = citylen+1
        while number > citylen:
            number = abs(int(random.gauss(0,100)))
        return self.data[number]
    
    def gamesetup(self):
        self.city = self.choose_city()
        self.city = [x.strip() for x in self.city.split('\t')]
        print "Your city to find is: " + self.city[1] + ", " + self.city[4]
        self.text.config(state="normal")
        self.text.delete("1.19", END)
        self.text.insert(END, self.city[1] + ", " + self.city[4] )
        self.text.config(state=DISABLED)
        self.score = 0


    def gameplay(self):
        if self.first_round != 0:
            self.canvas.delete(self.target)
        self.tot_score += self.distance_score()
        self.scoreText.config(state="normal")
        self.scoreText.delete("1.00", END)
        self.scoreText.insert(END, str(self.tot_score))
        self.scoreText.config(state=DISABLED)
        print "total score = " + str(self.tot_score)
        print type(self.city[3])
        self.target = self.canvas.create_image(int(self.city[3])-self.cross_width/2, int(self.city[2])-self.cross_height/2, image=self.cross, anchor='nw')
        self.canvas.tag_raise(self.target)
        print "wheeyyy" + self.city[2], self.city[3]
        self.first_round = 1
	self.change_to_small()
        if str(self.click[0]) == str(self.city[2]) and str(self.click[1]) == str(self.city[3]):
            self.gamesetup()
        else:
            self.gamesetup()

    def distance_score(self):
        xdist = int(self.click[0]) - int(self.city[2])
        ydist = int(self.click[1]) - int(self.city[3])
        dist = int(math.sqrt((xdist + ydist)**2))
        score = 30 - dist*2
        if score < 0:
            score = 0
        print "round score = " + str(score)
        return score
        

root = Tk()
myGeoGame = GeoGame(root)
root.mainloop()
