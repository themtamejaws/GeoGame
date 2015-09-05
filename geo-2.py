from PIL import ImageTk
from PIL import Image
from Tkinter import Tk, Label, Button, Frame, Text, END, DISABLED, RIGHT, TOP, BOTTOM, LEFT, Canvas
import tkFont
import random
import math
                
class GeoGame(Frame):

    def __init__(self, master):
        self.master = master
        self.master.title("GeoGame")
	self.master.protocol('WM_DELETE_WINDOW', self.close)
	
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

    def close(self):
	self.master.destroy()
	fileout = open("sorted2.txt", 'w')
	for line in self.data:
	    seq = (str(x) for x in line)
	    seq = "\t".join(seq)
	    fileout.write(seq)
	    fileout.write("\n")

    def change_to_big(self):
	self.canvas.delete(self.label)
	self.upper = (self.click[1]*10) - 300
	self.left = (self.click[0]*10) - 600
	right = (self.click[0]*10) + 600
	lower = (self.click[1]*10) + 300
	self.crop_big = self.bigim.crop((self.left, self.upper, right, lower))
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
        f = open('sorted2.txt', 'r').readlines()
        data = []
        for line in f:
	    line = [x.strip() for x in line.split("\t")]
            data.append(line)
        #f.close()
        return data

    def choose_city(self):
        citylen = len(self.data)
        self.number = random.randint(0, citylen)
	#self.number = citylen+1
	#while self.number > citylen:
        #    self.number = abs(int(random.gauss(0,100)))
        return self.data[self.number]
    
    def gamesetup(self):
        self.city = self.choose_city()
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
        self.change_to_small()
	x = int(int(self.city[3])/10)
	y = int(int(self.city[2])/10)

	self.target = self.canvas.create_image(int(x)-self.cross_width/2, int(y)-self.cross_height/2, image=self.cross, anchor='nw')
        self.canvas.tag_raise(self.target)
        self.first_round = 1
        self.gamesetup()
	self.update_difficulty()

    def distance_score(self):
        offsetx = self.click[0]+self.left
	offsety = self.click[1]+self.upper
	
	ydist = int(offsety) - int(self.city[2])
        xdist = int(offsetx) - int(self.city[3])
        self.dist = int(math.sqrt((xdist)**2 + (ydist)**2))
	score = int(500 - self.dist**1.5)
        if score < 0:
            score = 0
        print "round score = " + str(score)
        return score
        
    def update_difficulty(self):
	self.data[self.number][7] = (float(self.city[7])*float(self.city[6]) + self.dist) / (float(self.city[6]) + 1)
	self.data[self.number][6] = int(self.data[self.number][6]) + 1

root = Tk()
myGeoGame = GeoGame(root)
root.mainloop()
