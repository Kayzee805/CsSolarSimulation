from body import Body

import matplotlib.pyplot as plt 
from numpy.linalg import norm
import math
import numpy as np  
from matplotlib.animation import FuncAnimation


class System(object):   
    def __init__(self,planets,steps):
        self.planets = planets                      #planets is a list of celestial bodies
        self.steps = steps                          #total number of steps
        self.total = np.zeros(self.steps)           #Where total energy will be stored, total[i] = kinetic[i]+potential[i]
        self.kinetic = np.zeros(self.steps)
        self.potential = np.zeros(self.steps)
        self.time = 0                               #will initialise it once in one of the update methods, already initialised in body class

        self.lists = []                             #where lists of all positions will be stored

    def calcAcc(self,i):
        acc = 0
        g = 6.67e-11

        for j in self.planets:
            if i!=j:                                #Will calculate the acceleration on a body by all other bodies apart from itself
                pos = j.position - i.position
                magPos = norm(pos)                  #Normalising to find the magnitude of the position
                acc += (j.mass*pos)/magPos**3
        
        return acc*g                                   #Gravitaional potential is multipied at the end


    def calcKinetic(self,i):                        #Calculated and returns kinetic energy, using Ek= .5*mv^2
        ek = 0
        normVel = norm(i.velocity)
        ek= 0.5*i.mass*normVel**2

        return ek



    def history(self):

        lists = []                                  #An empty dummy array where positions will be stored
        kinetic = np.zeros(self.steps)
        potential = np.zeros(self.steps)
        total = np.zeros(self.steps)                #empty dummy arrays where energy will be stored

        for i in range(0,self.steps):
            ek = 0
            ep=0
            lists.append([])                        #Adding a list to every index of the list, to make it a 2d array

            for j in self.planets:
                if(self.time == 0):
                    self.time = j.time              #initilising the timeStep here
                for k in self.planets:      
                    if j!=k:                        #Calculating the potential energy due to all other bodies here
                        magPos = norm(k.position - j.position)
                        ep+= (6.67e-11*j.mass*k.mass)/magPos
                
                #maybe im meant to calcualte all the nextAcc at once?

                if i==0:
                                                    #currentAcceleration and previousAccereation has been initialised to 0
                    lists[i].append(j.position)     #Appending the first position then calculating velcocity as beeman's algorithm suggest
                    j.nextAcc = self.calcAcc(j)
                    vel = j.calcVel()
                    j.velocity = vel
                else:
                
                    j.prevAcc = j.acceleration      #No need to calculated acceleration 3 times, just using the one we have already found
                    j.acceleration = j.nextAcc
                    pos = j.calcPos()
                    j.position = pos
                    lists[i].append(pos)
                    j.nextAcc = self.calcAcc(j)     #only calculating acceleration for the nextAcceleration only, and this will be currentAcceleration
                                                    #in the next time step, then previousAcceleration in the timestep after
                    vel = j.calcVel()
                    j.velocity = vel                
            



                ek += self.calcKinetic(j)           #Calls the function to calculate kinetic energy and adds it to ek
            
         
            kinetic[i] = ek
            potential[i] = -ep/2                    #potential *-1/2 to avoid double counting paris of bodies

            total[i] = kinetic[i] + potential[i]

                
        self.kinetic = kinetic
        self.potential = potential         
        self.total = total
        self.lists = lists                          #storing the dummy list to the acutal lists of the class
        return lists                                #Just have return here to check the values later on
    

    def plotEnergy(self):
        y = self.total                              #initiliasing y as the list of energy
        x = []
        for i in range(self.steps):
            x.append(i*self.time)                   #adding a x value for the same length as y, which is steps as well, then multiplying by time
                                                    #time== timeStep is same for all the bodies

        plt.xlabel("Time (Seconds)")
        plt.ylabel("Total Energy ( Joules)")                                    
        plt.plot(x,y)
        plt.show()
        
    def period(self,planetNumber):                  #to calculate the period of each planet
        num = 0
        for i in range(self.steps-1):
            if(self.lists[i][planetNumber][1]<0):
                if(self.lists[i+1][planetNumber][1]>0):     #makes it so if y is negative for i'th iteration, it orbits once if y is positive for i+1
                    print("period of planet: "+ self.planets[planetNumber].name + " = " + str(((i-num)*100000)/(60*60*24)))
                    num = i #had num for multiple periods   #to make sure that period is consistent
                    break


    def printEnergy(self):

        f = open("Energy.txt",'w')                  #creates a new text file called energy

        for i in range(0,len(self.total)):
            if i %500== 0:              #can choose to change the freq of prints here
                energy = self.total[i]
                string = ("\nTotal energy at step "+str(i)+" = "+ str(energy))
                
                #string+= ("\nKinetic energy = "+str(self.kinetic[i]))
                #string+=("\nPotential energy = "+ str(self.potential[i])+"\n\n")       #to double check kinetic and potential
                f.write(string)                     #writes out the string to the file

        f.close()

    def init(self):
        return self.patches         #initialiser for animator
 

    def animate(self,i):
        for j in range(len(self.planets)):
            self.patches[j].center = (self.lists[i][j][0],self.lists[i][j][1]) #updates the center every iteration for all planets
        return self.patches                                                     # i = step, j = body, [0] is the x position, [1] is the y position
    
  
    
    
    def run(self):
        fig = plt.figure()      #sets up the axes
        ax = plt.axes()
        self.patches = []

        for i in self.planets:  #adding all the planets to patches 
            self.patches.append(plt.Circle((i.position[0],i.position[1]),i.size,color = i.colour, animated = True))
        

        for i in range(0,len(self.patches)):    #then adding the patches to the axes
            ax.add_patch(self.patches[i])
        
        #setting up the axes
        ax.axis('scaled')
        size = 5e11
        ax.set_xlabel("X- axis (meters) ")
        ax.set_ylabel("Y- axis (meters)")
        ax.set_xlim(-size,size)
        ax.set_ylim(-size,size)

        #creating the animator

        anim = FuncAnimation(fig,self.animate, init_func = self.init, frames = self.steps,repeat = False, interval =50 , blit = True)
        plt.show()
     



def main():
    # mass,orbitalRadius,size, name, colour
    path = "c:/Users/kayze/Desktop/Computer Simulation/submit/input.txt"
    #path to where your file is located at, as of now i just put my own path
    bodies = []
    file = open(path, "r")
    

    for line in file:
        fields = line.split(",")
        mass = float(fields[0])
        radius = float(fields[1])
        size = float(fields[2])
        name = fields[3]
        a = fields[4]                   
        colour = a[0]                    #first character of a string, a letter is read as a string as well

        bodies.append(Body(mass,radius,size,name,colour))   #adding each of the planets to the list of planets
    

    file.close()
    #steps = 369   to reach mars
    #steps = 2460    to come back to earth
    steps = int(input("Total number of iterations/steps? "))
    a = System(bodies,steps)
    lists = a.history()         #to initiliase the lists of position and also to double check it myself
    a.run()
    a.plotEnergy()
    a.period(3)
    for i in range(len(bodies)):
        if bodies[i].name != "Sun":
            a.period(i)

    a.printEnergy()

"""
    for i in range(steps):
        if (norm(lists[i][4]-lists[i][5])) <100000000:
            print("its close at"+str(i))

    print(norm(lists[369][5]-lists[369][4]))
    print(lists[369][5])
    print(lists[369][4])"""

    #takes 8 earth years to come back



main()


"""

    sun = Body(1.989e30,1,20e9, "Sun",'y')
    mars = Body(6.39e23, 227.92e9,3.39e9, "Mars" , 'r')
    mercury = Body(3.285e23,57.91e9,2.4e9,"mercury",'b')
    venus = Body(4.87e24,108.21e9,5.05e9,"venus",'k')
    earth = Body(5.972e24,149.6e9,6.3e9,"earth",'g')
"""