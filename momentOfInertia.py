#!I copied from NeHe/lesson5.py
from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *
from math import *
import sys

# Some api in the chain is translating the keystrokes to this octal string
# so instead of saying: ESCAPE = 27, we use the following.
ESCAPE = '\033'

# Number of the glut window.
window = 0

# Rotation angle for the triangle. 
rtri = 0.0

# Rotation angle for the quadrilateral.
rquad = 0.0

# A general OpenGL initialization function.  Sets all of the initial parameters. 
def InitGL(Width, Height):				# We call this right after our OpenGL window is created.
    glClearColor(0.0, 0.0, 0.0, 0.0)	# This Will Clear The Background Color To Black
    glClearDepth(1.0)					# Enables Clearing Of The Depth Buffer
    glDepthFunc(GL_LESS)				# The Type Of Depth Test To Do
    glEnable(GL_DEPTH_TEST)				# Enables Depth Testing
    glShadeModel(GL_SMOOTH)				# Enables Smooth Color Shading
	
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()					# Reset The Projection Matrix
										# Calculate The Aspect Ratio Of The Window
    gluPerspective(45.0, float(Width)/float(Height), 0.1, 100.0)

    glMatrixMode(GL_MODELVIEW)

# The function called when our window is resized (which shouldn't happen if you enable fullscreen, below)
def ReSizeGLScene(Width, Height):
    if Height == 0:						# Prevent A Divide By Zero If The Window Is Too Small 
	    Height = 1

    glViewport(0, 0, Width, Height)		# Reset The Current Viewport And Perspective Transformation
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    gluPerspective(45.0, float(Width)/float(Height), 0.1, 100.0)
    glMatrixMode(GL_MODELVIEW)

g = 9.8 #gravitational acceleration
pi = 3.1415926535897
slope_length = 5.5
slope_width = 1.0
slope_height = 0.5
slope_angle = atan2(slope_height, slope_length)
plane_length = slope_length * 4
deltaT = 0.015
ring_radius = 0.3
ring_z = -slope_width/2.0
ring_center_x = 0.0
ring_center_y = slope_height + ring_radius
nob_at_ring = pi * 0.36
rotation_acceleration = 0.0  #radians/sec
rotation_speed = 0.0
mass_of_ring = 1.0
mass_of_nob = 8.0

def Initialize():
	ring_center_x = 0.0
	ring_center_y = slope_height + ring_radius
	nob_at_ring = 0.0
	rotation_acceleration = 0.0
	rotation_speed = 0.0

def DrawSlopeAndPlane():
	global slope_length, slope_width, slope_height, slope_angle, plane_length
	glBegin(GL_TRIANGLES);

	glColor3f(1.0,0.0,0.0)
	glVertex3f(0.0,0.0,0.0)						# p1
	glColor3f(0.0,1.0,0.0)
	glVertex3f(slope_length,0.0,0.0)			# p2
	glColor3f(0.0,0.0,1.0)
	glVertex3f(0.0,slope_height,0.0)			# p3

	glColor3f(0.0,1.0,0.0)
	glVertex3f(slope_length,0.0,0.0)			# p2
	glColor3f(1.0,0.0,0.0)
	glVertex3f(slope_length,0.0,-slope_width);	# p4
	glColor3f(0.0,0.0,1.0)
	glVertex3f(0.0,slope_height,0.0);			# p3

	glColor3f(1.0,0.0,0.0)
	glVertex3f(slope_length,0.0,-slope_width)	# p4
	glColor3f(0.0,1.0,0.0)
	glVertex3f(0.0,slope_height,-slope_width)	# p5
	glColor3f(0.0,0.0,1.0)
	glVertex3f(0.0,slope_height,0.0)			# p3
	
	glColor3f(1.0,0.0,0.0)
	glVertex3f(slope_length,0.0,-slope_width)	# p4
	glColor3f(0.0,0.0,1.0)
	glVertex3f(0.0,0.0,-slope_width)			# p6
	glColor3f(0.0,1.0,0.0)
	glVertex3f(0.0,slope_height,-slope_width)	# p5
	
	#plane
	glColor3f(0.0,1.0,0.0)
	glVertex3f(slope_length,0.0,0.0)			# p2
	glColor3f(0.0,0.0,1.0)						
	glVertex3f(plane_length,0.0,0.0)			# p7
	glColor3f(1.0,0.0,0.0)
	glVertex3f(plane_length,0.0,-slope_width)	# p8

	glColor3f(1.0,0.0,0.0)
	glVertex3f(plane_length,0.0,-slope_width)	# p8
	glColor3f(1.0,0.0,0.0)
	glVertex3f(slope_length,0.0,-slope_width)	# p4
	glColor3f(0.0,1.0,0.0)
	glVertex3f(slope_length,0.0,0.0)			# p2

	glEnd()

def DrawRing(x, y, z, nobAngle, radius):
	DEG2RAD = 3.1415926535/180
	glBegin(GL_LINE_LOOP);
	for i in range(360):
		degInRad = nobAngle + i*DEG2RAD
		green_intensity =  0.0
		blue_intesity = 0.0
		red_intensity =  1.0 - i / 360.0
		glColor3f(red_intensity,green_intensity,blue_intesity)
		glVertex3f(x+cos(degInRad)*radius,y + sin(degInRad)*radius,z)
	glEnd();

def GetCenterOfMass(geometricCenterX, geometricCenterY, z, radius, nobAngle, ringMass, nobMass):
	dToCenter = nobMass * radius / (ringMass + nobMass)
	x = geometricCenterX + dToCenter * cos(nobAngle)
	y = geometricCenterY + dToCenter * sin(nobAngle)
	DEG2RAD = 3.1415926535/180
	glBegin(GL_LINE_LOOP);
	for i in range(360):
		degInRad = nobAngle + i*DEG2RAD
		green_intensity =  1.0
		blue_intesity = 1.0
		red_intensity =  0.0
		glColor3f(red_intensity,green_intensity,blue_intesity)
		glVertex3f(x+cos(degInRad)*0.01,y + sin(degInRad)*0.01,z)
	glEnd();
	return x, y

#pointing out of screen is positive
def GetTorque(referenceX, massX, mass, g ):
	r = referenceX - massX
	torque = r * mass * g
	return torque

def GetMomentOfInertia(referenceX, referenceY, geometricCenterX, geometricCenterY, radius, nobAngle, ringMass, nobMass):
	momentOfInertiaOfRing = 1.5 * ringMass * radius * radius
	nobX = geometricCenterX + radius*cos(nobAngle)
	dx = nobX - referenceX
	momentOfInertiaOfNob = nobMass * dx*dx
	return momentOfInertiaOfRing + momentOfInertiaOfNob
	
# The main drawing function. 
def DrawGLScene():
	global g, pi, slope_length,  slope_angle, plane_length, deltaT, ring_radius, ring_z
	global ring_center_x, ring_center_y, nob_at_ring, rotation_acceleration, rotation_speed
	global rtri, rquad

	glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT);	# Clear The Screen And The Depth Buffer
	glLoadIdentity();					# Reset The View
	glTranslatef(-1.3,-1.0,-3.0);			
	glRotatef(rtri,0.0,1.0,0.0);		# Rotate The Pyramid On It's Y Axis

	DrawSlopeAndPlane()
	
	#calculate ring's position
	rolledAngle = rotation_speed * deltaT
	rolledDistance = rolledAngle * ring_radius
	nob_at_ring -= rolledAngle
	if nob_at_ring < -2 * pi:
		nob_at_ring += 2 * pi

	if ring_center_x > slope_length + plane_length:
		#reset to initial state
		Initialize()
	else:
		#calculate angular acceleration
		if ring_center_x > slope_length:
			x_distance = rolledDistance
			y_distance = 0.0
		else:
			#still on the slop
			cos_theta = cos(slope_angle)
			sin_theta = sin(slope_angle)
			x_distance = rolledDistance * cos_theta
			y_distance = -rolledDistance * sin_theta

		ring_center_x += x_distance
		ring_center_y += y_distance

		if ring_center_x > slope_length:
			referenceX = ring_center_x
			referenceY = ring_center_y - ring_radius
		else:
			referenceX = ring_center_x - ring_radius * sin(slope_angle)
			referenceY = ring_center_y - ring_radius * cos(slope_angle)

		cx, cy = GetCenterOfMass(ring_center_x, ring_center_y, ring_z, ring_radius, nob_at_ring, mass_of_ring, mass_of_nob)
		torque = GetTorque(referenceX, cx, mass_of_ring + mass_of_nob, g)
		I = GetMomentOfInertia(referenceX, referenceY, ring_center_x, ring_center_y, ring_radius, nob_at_ring, mass_of_ring, mass_of_nob)
		rotation_acceleration = -torque / I
		rotation_speed += rotation_acceleration * deltaT

	DrawRing(ring_center_x, ring_center_y, ring_z, nob_at_ring, ring_radius)

	# What values to use?  Well, if you have a FAST machine and a FAST 3D Card, then
	# large values make an unpleasant display with flickering and tearing.  I found that
	# smaller values work better, but this was based on my experience.
	rtri  = rtri + 0.15   # Increase The Rotation Variable For The Triangle
	rquad = rquad - 0.15 # Decrease The Rotation Variable For The Quad

	#  since this is double buffered, swap the buffers to display what just got drawn. 
	glutSwapBuffers()

# The function called whenever a key is pressed. Note the use of Python tuples to pass in: (key, x, y)  
def keyPressed(*args):
	# If escape is pressed, kill everything.
    if args[0] == ESCAPE:
	    sys.exit()

def main():
	global window
	glutInit(sys.argv)

	Initialize()
	
	# Select type of Display mode:   
	#  Double buffer 
	#  RGBA color
	# Alpha components supported 
	# Depth buffer
	glutInitDisplayMode(GLUT_RGBA | GLUT_DOUBLE | GLUT_DEPTH)
	
	# get a 640 x 480 window 
	glutInitWindowSize(640, 480)
	
	# the window starts at the upper left corner of the screen 
	glutInitWindowPosition(0, 0)
	
	# Okay, like the C version we retain the window id to use when closing, but for those of you new
	# to Python (like myself), remember this assignment would make the variable local and not global
	# if it weren't for the global declaration at the start of main.
	window = glutCreateWindow("Moment of inertia")

   	# Register the drawing function with glut, BUT in Python land, at least using PyOpenGL, we need to
	# set the function pointer and invoke a function to actually register the callback, otherwise it
	# would be very much like the C version of the code.	
	glutDisplayFunc(DrawGLScene)
	
	# Uncomment this line to get full screen.
	# glutFullScreen()

	# When we are doing nothing, redraw the scene.
	glutIdleFunc(DrawGLScene)
	
	# Register the function called when our window is resized.
	glutReshapeFunc(ReSizeGLScene)
	
	# Register the function called when the keyboard is pressed.  
	glutKeyboardFunc(keyPressed)

	# Initialize our window. 
	InitGL(640, 480)

	# Start Event Processing Engine	
	glutMainLoop()

# Print message to console, and kick off the main to get it rolling.
print "Hit ESC key to quit."
main()
    	
