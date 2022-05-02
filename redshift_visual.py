from vpython import *
#GlowScript 3.2 VPython

# Author: Daniel Opara
# Purpose: To provide a visual demonstration of the redshift of light waves/particles near Schwarzschild black holes

# Based on program written by Ruth Chabay to demonstrate sinusoidal waves
# Original program can be found here:
# https://www.glowscript.org/#/user/matterandinteractions/folder/matterandinteractions/program/23-sinusoidal-wave-wavelength

scene2 = canvas(width=999, height=599, background = color.white, title="""
The emitted wave""")
L_scene2 = label(pos=vec(400,400,0),
    text="""Wavelength: 500 nm
    Schwarzschild Radius: 0 km"""
    , xoffset=20,
    yoffset=50, space=30,
    height=16, border=4,
    font='sans')

scene = canvas(title='The observed wave')
scene.width = 1000
scene.height = 600
scene.background = color.white
L_scene = label(pos=vec(400,400,0),
    text="""Wavelength: 500 nm
    Redshift Ratio: 0
    Schwarzschild Radius: 0 km"""
    , xoffset=20,
    yoffset=50, space=30,
    height=16, border=4,
    font='sans', canvas=scene)
# constants
E0 = 1e4
c = 3e8     

class Arrows:
    def __init__(self, drawing_canvas, observed):
        self.drawing_canvas = drawing_canvas
        drawing_canvas.range = 1*500
        self.observed = observed
        
        
    # class variables that relate directly to the wave/particle
    # these values are measured from the emitted source at the r-coordinate
    wavelength = 500 #unit is nanometers (nm)
    observed_wavelength = 0 #observed from the shell observer
    frequency = c/wavelength
    period = 1/frequency
    dt = 3e-4*period
    t = 0
    arrowlist=[]
    
    # class variables that relate directly to the wave/particle
    # these values are measured from the shell observer at infinity
    observed_wavelength = 0
    observed_frequency = 0
    
    radius_of_emitted = 0 #this is the radius at which the wave/particle is emitted with respect to the bh radius, can also be interpreted as the r-coordinate of the wave/particle
    redshift_ratio = 0 #is also known as the z-value
    
    # class variables that relate directly to the black hole
    bh_mass = 0
    bh_schwarzschildradius = 0
    

    # updatetime is required for showing the change of arrows at a single point over time
    def updatetime(self):
        self.t = self.t + self.dt
        
    # the function was made for dealing with parts of the program that needed the 
    # observed wavelength before it was assigned an actual value
    def use_appropriate_wavelength(self):
        if self.observed == False:
            wavelength = self.wavelength
        else:
            if self.observed_wavelength == 0:
                wavelength = self.wavelength
            else:
                wavelength = self.observed_wavelength
                
        return wavelength
    
    # the function was made for dealing with parts of the program that needed the 
    # observed frequency before it was assigned an actual value
    def use_appropriate_frequency(self):
        if self.observed == False:
            frequency = self.frequency
        else:
            if self.observed_frequency == 0:
                frequency = self.frequency
            else:
                frequency = self.observed_frequency
                
        return frequency
        
    
    # calculates the radius of the black hole given mass is in solar mass
    def calculate_schwarzschildradius(self, new_bh_mass):
        new_radius = 3 * new_bh_mass
        self.bh_schwarzschildradius = new_radius
        self.bh_mass = new_bh_mass
    
    # changes the r-coordinate or location of the wave/particle in relation to the center of the black hole
    def change_r_coordinate(self, new_r):
        self.radius_of_emitted = new_r
    
    # calculates the redshift ratio of the wave/particle, used to find the observed wavelength for shell observers
    def calculate_redshift_ratio(self):
        if (self.radius_of_emitted < 0):
            print("input an r coordinate")
        else:
            if self.radius_of_emitted < self.bh_schwarzschildradius:
                self.redshift_ratio = 0
            else:
                value_of_sqrt = sqrt(1-(self.bh_schwarzschildradius/self.radius_of_emitted))
                zed = (1/value_of_sqrt)-1 #named zed bc of weird conflicts with glowscript
                self.redshift_ratio = zed
        
    
    # calculates the observed wavelength of a wave/particle emitted near a black hole
    #  to an observer far away from the black hole (observed from infinity)
    def calculate_observedmeasurements(self):
        if self.redshift_ratio == 0:
            pass
        else:
            self.observed_wavelength = (self.redshift_ratio * self.wavelength) + self.wavelength
            self.observed_frequency = c/self.observed_wavelength
        
        
    # changing the wavelength of the wave requires updating all values dependent on that measurement
    # updates measurement updates all the class variables dependednt on wavelength
    def updatemeasurements(self, new_wavelength):
        wavelength = self.use_appropriate_wavelength()
        self.wavelength = new_wavelength
        self.frequency = self.frequency
        self.period = 1/self.frequency
        self.dt = 3e-4*self.period
        self.t = 0
        
    # updates the text box for each scene with information describing the wave/particle if it is changed
    def updatetext(self):
        if self.observed == True:
            new_text = f"""Wavelength: {self.use_appropriate_wavelength()} nm
            Redshift Ratio: {self.redshift_ratio}
            Schwarzschild Radius: {self.bh_schwarzschildradius} km
            Frequency: {self.observed_frequency} hertz (Hz)"""
            global L_scene
            L_scene.text = new_text
        else:
            new_text = f"""Wavelength: {self.wavelength} nm
            Schwarzschild Radius: {self.bh_schwarzschildradius} km
            Frequency: {self.frequency}"""   
            global L_scene2
            L_scene2.text = new_text

        
    # sets the arrowlist of the class to be accurate with respect to the wavelength of object instance
    def constructarrows(self):
        wavelength = self.use_appropriate_wavelength()
        #Make a list of observation locations along a line
        pointlist=arange(-3*wavelength*10, 3*wavelength*10, wavelength/16)
        temp_arrowlist=[]
        
        #Loop over observation locations and create electric and magnetic field arrows there
        #Add the arrows to a list
        for x in pointlist:
            Earrow=arrow(pos=vector(x,0,0), color=color.orange, shaftwidth=wavelength/40, canvas=self.drawing_canvas)
            Earrow.B=arrow(pos=vector(x,0,0), color=color.cyan, shaftwidth=wavelength/40, canvas=self.drawing_canvas)
            temp_arrowlist.append(Earrow)
            if abs(x) < 0.03*wavelength:
                Earrow.color = color.red
                Earrow.B.color = color.black 
        self.arrowlist = temp_arrowlist
        
    # constructs a ruler with respect to the wavelength of object instance 
    def constructruler(self):
        wavelength = self.use_appropriate_wavelength()
        yy = -wavelength*.65
        xx = -0.5*wavelength
        dyy = wavelength/5
        pts = [vector(xx,yy+dyy,0),vector(xx,yy-dyy,0),vector(xx,yy,0),vector(xx+wavelength,yy,0),
               vector(xx+wavelength,yy+dyy,0),vector(xx+wavelength,yy-dyy,0)]
               
        return pts
        

# Set up arrow object along with ruler
myArrows_observed = Arrows(drawing_canvas=scene, observed=True)
myArrows_emitted = Arrows(drawing_canvas=scene2, observed=False)
run = True
ruler_observed = curve(color=color.green, pos=myArrows_observed.constructruler(),radius=myArrows_observed.use_appropriate_wavelength()/30, canvas=scene)
ruler_emitted = curve(color=color.green, pos=myArrows_emitted.constructruler(),radius=myArrows_emitted.use_appropriate_wavelength()/30, canvas=scene2)


# Handles input for changing the wavelength of the myArrows object 
def changewavelength(new_wavelength): 
    if new_wavelength.number == None:
        print("Please type a number")
    else:
        # updates the values of class variable related to the wave/particle
        myArrows_observed.updatemeasurements(new_wavelength.number)
        myArrows_emitted.updatemeasurements(new_wavelength.number)
        
        # changes the observed wavelength of the particle/wave and other measurements
        # dependent on the wavelength for the shell observer
        myArrows_observed.calculate_observedmeasurements()
        
        # updates the text boxes
        myArrows_observed.updatetext()
        myArrows_emitted.updatetext()
        
        # remakes the arrows with respect to the new values of the class variables
        myArrows_observed.constructarrows()
        myArrows_emitted.constructarrows()
        
        # creates a list of points in space that will serve for creating the ruler
        ptslist_observed = myArrows_observed.constructruler()
        ptslist_emitted = myArrows_emitted.constructruler()
        global ruler_observed
        global ruler_emitted
        
        # clears any points in the ruler from previous methods 
        ruler_observed.clear()
        ruler_emitted.clear()
        
        # recreates the rulers with respect to the new values of the class variables
        ruler_observed = curve(color=color.green, pos=ptslist_observed,radius=myArrows_observed.use_appropriate_wavelength()/30, canvas=scene)
        ruler_emitted = curve(color=color.green, pos=ptslist_emitted,radius=myArrows_emitted.use_appropriate_wavelength()/30, canvas=scene2)
input_wavelength = winput(bind=changewavelength, text=500)
scene.append_to_caption(""" Use the text box to input emitted wavelength in nanometers (nm).
""")

# Handles input for changing the mass of the black hole for the myArrows object 
def changebh_mass(new_mass): 
    if new_mass.number == None:
        print("Please type a number")
    else:
        myArrows_observed.calculate_observedmeasurements()
        # calculates the radius of the black hole given its mass and recalculates
        # the redshift ratio if it changes so long that input for the r-coordinate exists
        myArrows_observed.calculate_schwarzschildradius(new_mass.number)
        if (myArrows_observed.radius_of_emitted != 0):
            myArrows_observed.calculate_redshift_ratio()
            
        
        myArrows_observed.updatemeasurements(new_wavelength.number)
        
        myArrows_observed.updatetext()
        myArrows_emitted.updatetext()
        
        myArrows_observed.constructarrows()
        
        ptslist_observed = myArrows_observed.constructruler()
        global ruler_observed
        ruler_observed.clear()
        ruler_observed = curve(color=color.green, pos=ptslist_observed,radius=myArrows_observed.use_appropriate_wavelength()/30, canvas=scene)
input_bh_mass = winput(bind=changebh_mass, text=0)
scene.append_to_caption(""" Use the text box to input the black hole mass in terms of solar mass (M).
""")

# Handles input for changing the r-coordinate location of the wave/particle being
# emitted for the myArrows object 
def change_r_coordinate(new_r): 
    if new_r.number == None:
        print("Please type a number")
    else:
        # chnage the r-coordinate before calculing the redshift
        myArrows_observed.change_r_coordinate(new_r.number)
        myArrows_observed.calculate_redshift_ratio()
        
        # recalculate the observed wavelenth 
        myArrows_observed.calculate_observedmeasurements()
        
        myArrows_observed.updatetext()
        myArrows_emitted.updatetext()
        
        myArrows_observed.updatemeasurements(new_wavelength.number)
        myArrows_observed.constructarrows()
        
        ptslist_observed = myArrows_observed.constructruler()
        global ruler_observed
        ruler_observed.clear()
        ruler_observed = curve(color=color.green, pos=ptslist_observed,radius=myArrows_observed.use_appropriate_wavelength()/30, canvas=scene)
input_bh_mass = winput(bind=change_r_coordinate, text=0)
scene.append_to_caption(""" Use the text box to input the r-coordinate from which the wave/particle is being emitted hole in kilometers (km).

The green marker indicates the length of one wavelength.
""")

scene.append_to_caption("""


**This program assumes you are a shell observer making measurements from 
a static Schwarzschild black hole when performing calculations. At the start of
the program, the wave is nowhere near a black hole thus all measurements related
to redshifts and the black hole are set to 0.


""")



def B_Runbutton(b):
    global run
    run = not run
    if run:
        b.text = "Pause program"
    else:
        b.text = "Resume program"
button(text="Pause", bind=B_Runbutton)


# KEEP THE NEXT FOUR LINES UNDER ALL COSTS, VERY NECESSARY TO INITIALIZE THIS ENTIRE THING
myArrows_observed.constructarrows()
myArrows_emitted.constructarrows()
glob_arrowlist = myArrows_observed.arrowlist
foo_arrowlist = myArrows_emitted.arrowlist


#Dynamics of wave motion
while True:
    rate(1000)
    if not run: continue
    #Loop over arrows and update their axes according to planewave equation
    for Earrow in glob_arrowlist:
        E = vector(0,E0*cos(2*pi*(myArrows_observed.use_appropriate_frequency()*myArrows_observed.t-Earrow.pos.x/myArrows_observed.use_appropriate_wavelength())),0)
        B = vector(0,0,E.y/c)
        Earrow.axis = E/40
        Earrow.B.axis = B*(c/50)
    for Earrow in foo_arrowlist:
        E = vector(0,E0*cos(2*pi*(myArrows_emitted.use_appropriate_frequency()*myArrows_emitted.t-Earrow.pos.x/myArrows_emitted.use_appropriate_wavelength())),0)
        B = vector(0,0,E.y/c)
        Earrow.axis = E/40
        Earrow.B.axis = B*(c/50)
    myArrows_observed.updatetime()
    myArrows_emitted.updatetime()
