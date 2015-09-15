from PIL import ImageTk
from PIL import Image
from Tkinter import Tk, Label, Button, Frame, Text, END, DISABLED, RIGHT, TOP, BOTTOM, LEFT, Canvas
import tkFont
import random
import math
from math import radians, cos, sin, asin, sqrt
import time
import sys
import database
                
class GeoGame(Frame):

    def __init__(self, master):
        self.master = master
        self.master.title("GeoGame")
        self.master.protocol('WM_DELETE_WINDOW', self.close)
    
        self.smallim = Image.open("textures/maps/medium_map.jpg")
        self.bigim = Image.open("textures/maps/big_map.jpg")
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

        self.crosshairs = Image.open("textures/crosshairs/targetcrosshair.gif") #GIFs ONLY, PNG's transparency doesn't work
        self.crosshairs2 = Image.open("textures/crosshairs/clickcrosshair.gif")
        self.cross_width, self.cross_height = self.crosshairs.size
        self.cross_width2, self.cross_height2 = self.crosshairs2.size
        self.cross = ImageTk.PhotoImage(self.crosshairs)
        self.cross2 = ImageTk.PhotoImage(self.crosshairs2)
        self.first_round = 0
        self.zoomed = False        

        self.d = database.Database()
        self.tot_score = 0
        self.level = 1
        self.level_pass = self.max_score()
        self.difficulty = 50
        self.go_number = 1
        self.level_score = 0
        self.asked_index = [ (len(self.d.data)+1)]

        self.text = Text(self.bottomFrame, height=1, width=40, font=self.customFont)
        self.text.pack(side=LEFT)
        self.scoreText = Text(self.bottomFrame, height=1,width=10)
        self.scoreText.pack(side=RIGHT)
        self.scoreText.insert(END, str(self.tot_score))
        self.scoreText.config(state=DISABLED)
        self.scoreLabel = Label(self.bottomFrame, text="Total Score")
        self.scoreLabel.pack(side=RIGHT)
        self.text.insert(END, "Your next city is: ")
        self.text.config(state=DISABLED)
        self.levelText = Text(self.bottomFrame, height=1, width=10)
        self.levelText.pack(side=RIGHT)
        self.levelText.insert(END, str(self.level_score) + "/" + str(int(self.max_score())))
        self.levelText.config(state=DISABLED)
        self.levelLabel = Label(self.bottomFrame, text='Level 1 Score')
        self.levelLabel.pack(side=RIGHT)
        
        self.gamesetup()
        
    def close(self):
        self.master.destroy()
        self.d.close()

    def zoom_in(self):
        self.canvas.delete(self.label)
        self.zoomposition_x = self.click[0] - 60
        self.zoomposition_y = self.click[1] - 30
        self.upper = (self.click[1]*10) - 300
        self.left = (self.click[0]*10) - 600
        right = (self.click[0]*10) + 600
        lower = (self.click[1]*10) + 300
        self.crop_big = self.bigim.crop((self.left, self.upper, right, lower))
        self.crop_big2 = ImageTk.PhotoImage(self.crop_big)
        self.zoom = self.canvas.create_image(0, 0, image=self.crop_big2, anchor='nw')
        self.zoomed = True  

    def zoom_out(self):
        self.canvas.delete(self.zoom)
        self.label = self.canvas.create_image(0,0, image=self.im2, anchor='nw') 
        self.zoomed = False

    def callback(self, event):
        self.click = [event.x, event.y]
        if self.zoomed == False:
            self.zoom_in()
        else:
            x = int(int(self.city.xcord))-self.left
            y = int(int(self.city.ycord))-self.upper

            self.target3 = self.canvas.create_image(x - self.cross_width/2, y - self.cross_height/2,image=self.cross, anchor='nw')
            self.target4 = self.canvas.create_image(self.click[0] - self.cross_width2/2, self.click[1]-self.cross_height2/2, image=self.cross2, anchor='nw') 
            self.master.update()
            time.sleep(2)
            self.canvas.delete(self.target3)
            self.gameplay()
    
    def gamesetup(self):
        self.city, self.asked_index = self.d.choose_city(self.asked_index, self.difficulty)
        self.text.config(state="normal")
        self.text.delete("1.19", END)
        self.text.insert(END, self.city.cityname + ", " + self.city.country )
        self.text.config(state=DISABLED)
        self.score = 0

    def gameplay(self):
        if self.first_round != 0:
            self.canvas.delete(self.target)
        go_score = self.distance_score()
        self.tot_score += go_score
        self.level_score += go_score

        self.scoreText.config(state="normal")
        self.scoreText.delete("1.00", END)
        self.scoreText.insert(END, str(self.tot_score))
        self.scoreText.config(state=DISABLED)
        self.levelText.config(state="normal")
        self.levelText.delete("1.00", END)
        self.levelText.insert(END, str(self.level_score) + "/" + str(int(self.max_score())))
        self.levelText.config(state=DISABLED)

        self.zoom_out()
        
        x = int(int(self.city.xcord)/10)
        y = int(int(self.city.ycord)/10)
        self.x_click = self.zoomposition_x + int(self.click[0]/10)
        self.y_click = self.zoomposition_y + int(self.click[1]/10)

        self.target = self.canvas.create_image(int(x)-self.cross_width/2, int(y)-self.cross_height/2, image=self.cross, anchor='nw')

        self.target2 = self.canvas.create_image(int(self.x_click)-self.cross_width2/2, int(self.y_click)-self.cross_height2/2, image=self.cross2, anchor='nw')

        self.canvas.tag_raise(self.target2)
        self.first_round = 1
        self.city.update_difficulty(self.dist)
        self.go_number += 1

        if self.go_number == 10:
            if self.level_score > self.level_pass:
                self.level_up()
            else:
                self.level_fail()
        self.gamesetup()

    def distance_score(self):
        self.offset_x = float(self.click[0]+self.left)
        self.offset_y = float(self.click[1]+self.upper)

        click_long = (self.offset_x - 6000) * 0.03
        click_lat = (3000 - self.offset_y) * 0.03

        city_long = (int(self.city.xcord) - 6000) * 0.03
        city_lat = (3000 - int(self.city.ycord)) * 0.03

        self.dist = self.global_distance(click_long, click_lat, city_long, city_lat)

        if self.dist == 0:
            score = self.max_score()
        else:
            score = int( self.max_score() / (self.dist**0.5) )

        if score < 0:
            score = 0
        print "You scored: " + str(score)
        return score

    def global_distance(self, lon1, lat1, lon2, lat2):
        """
        Calculate the great circle distance between two points 
        on the earth (specified in decimal degrees)
        """
        # convert decimal degrees to radians 
        lon1, lat1, lon2, lat2 = map(radians, [lon1, lat1, lon2, lat2])

        # haversine formula 
        dlon = lon2 - lon1 
        dlat = lat2 - lat1 
        a = sin(dlat/2)**2 + cos(lat1) * cos(lat2) * sin(dlon/2)**2
        c = 2 * asin(sqrt(a)) 
        r = 6371 # Radius of earth in kilometers. Use 3956 for miles
        return c * r

    def level_up(self):
        self.level += 1
        self.levelLabel.config(text="Level " + str(self.level) + " Score")
        self.level_pass = self.max_score()
        print "LEVEL UP, Begin Level " + str(self.level)
        self.difficulty += 50
        self.go_number = 1
        self.level_score = 0
        self.levelText.config(state="normal")
        self.levelText.delete("1.00", END)
        self.levelText.insert(END, str(self.level_score) + "/" + str(int(self.max_score())))
        self.levelText.config(state=DISABLED)

    def level_fail(self):
        self.level = 1
        self.levelLabel.config(text="Level " + str(self.level) + " Score")
        self.level_pass = self.max_score()
        print "YOU FAILED, Begin Level 1"
        self.difficulty = 50
        self.go_number = 1
        self.level_score = 0
        self.tot_score = 0
        self.scoreText.config(state="normal")
        self.scoreText.delete("1.00", END)
        self.scoreText.insert(END, str(self.tot_score))
        self.scoreText.config(state=DISABLED)
        self.levelText.config(state="normal")
        self.levelText.delete("1.00", END)
        self.levelText.insert(END, str(self.level_score) + "/" + str(int(self.max_score())))
        self.levelText.config(state=DISABLED)

    def max_score(self):

        return int(1000 * (1.2 ** (self.level-1)))
        
root = Tk()
myGeoGame = GeoGame(root)
root.mainloop()


