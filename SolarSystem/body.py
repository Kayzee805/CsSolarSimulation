import numpy as np 
from numpy.linalg import norm
import math



class Body(object):
    def __init__(self,mass,radius,size,name,colour):
        self.mass = mass
        self.radius = radius
        self.size = size
        self.name = name
        self.colour = colour
        starMass = 1988500e24
        self.time = 100000
        self.acceleration = 0
        self.prevAcc = 0
        self.nextAcc = 0

        if self.name=="Sun":
            self.position = np.array([0,0])
            self.velocity = np.array([0,0])
        
        elif self.name == "Viking":
            self.position = np.array([self.radius,0])
           # self.velocity = np.array([3500,29669.3+4000])      #touches but really late
            self.velocity = np.array([3900,29669.3+3900])      #touches but really late

        else:
            self.position = np.array([self.radius,0])
            vel = math.sqrt((6.67e-11*starMass)/self.radius)
            self.velocity = np.array([0,vel])

    

    def calcPos(self):
        newPos = self.position +self.velocity*self.time + 1/6*(4*self.acceleration - self.prevAcc)*(self.time**2)
        #newPos = self.velocity*self.time +self.position
        self.position = newPos
        return newPos
    
    def calcVel(self):
        newVel = self.velocity + 1/6* (2*self.nextAcc +5*self.acceleration - self.prevAcc)*self.time
        #newVel = self.velocity+ self.acceleration*self.time
        self.velocity = newVel
        return newVel