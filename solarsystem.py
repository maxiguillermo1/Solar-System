import sys,gc
from OpenGL.GL       import *
from OpenGL.GLUT     import *
from OpenGL.GLU      import *
from PIL.Image       import *

# Create a global variable to store the light status (On or Off)
light_status = True

# rotation of each object in scene 
window       = 0
rot          = 0.0
rot2         = 0.0
rot3         = 0.0
rot4         = 0.0
rot5         = 0.0
rot6         = 0.0
rot7         = 0.0
rot8         = 0.0

# Define the ambient light color (RGB values between 0.0 and 1.0)
LightAmb     = (0.7, 0.7, 0.7)  

# Define the diffuse light color (RGB values between 0.0 and 1.0)
LightDif     = (1.0, 1.0, 0.0)  

# Define the light position (x, y, z, w)
# The position is specified in 3D space, and the 'w' component is set to 1.0 for a positional light
LightPos     = (4.0, 4.0, 6.0, 1.0)  

xrot = yrot = 0.0  # Set initial rotation angles to 0.0

xrotspeed = yrotspeed = 0.0  # Set initial rotation speeds to 0.0
zoom = -3.0  # Set initial zoom value to -3.0
height = 0.5  # Set initial height value to 0.5

textures = {}  # Initialize an empty dictionary to store textures

# Create a keyboard function to process key presses
def keyboard(key, x, y):
    global light_status

    # If the 'l' key is pressed, toggle the light
    if key == b'l':
        light_status = not light_status

        if light_status:
            glEnable(GL_LIGHTING)
            print('Lighting Enabled')
        else:
            glDisable(GL_LIGHTING)
            print('Lighting Disabled')

    glutPostRedisplay()  # Redraw the scene after state changes

def LoadTextures(fname):

    if textures.get( fname ) is not None:
        return textures.get( fname )
    
    texture = textures[fname] = glGenTextures(1)

    image = open(fname)

    ix = image.size[0]
    iy = image.size[1]
    image = image.tobytes("raw", "RGBX", 0, -1)
    # Create Texture    
    glBindTexture(GL_TEXTURE_2D, texture)   # 2D texture (x and y size)
    
    glPixelStorei(GL_UNPACK_ALIGNMENT,1)
    glTexImage2D(GL_TEXTURE_2D, 0, 3, ix, iy, 0, GL_RGBA, GL_UNSIGNED_BYTE, image)
    glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_CLAMP)
    glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_CLAMP)
    glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_REPEAT)
    glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_REPEAT)
    glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_NEAREST)
    glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_NEAREST)
    glTexEnvf(GL_TEXTURE_ENV, GL_TEXTURE_ENV_MODE, GL_DECAL)
    return texture


# A general OpenGL initialization function.  Sets all of the initial parameters.
#  initialization of the rendering environment, depth, mapping, lighting
def InitGL(Width, Height):
    # Ensure the dimensions are valid
    if Width <= 0 or Height <= 0:
        raise ValueError("Invalid width or height for OpenGL initialization.")
    
    glClearColor(0.0, 0.0, 0.0, 0.0)    # This Will Clear The Background Color To Black
    glClearDepth(1.0)                    # Enables Clearing Of The Depth Buffer
    glClearStencil(0)
    glDepthFunc(GL_LEQUAL)               # The Type Of Depth Test To Do
    glEnable(GL_DEPTH_TEST)              # Enables Depth Testing
    glShadeModel(GL_SMOOTH)              # Enables Smooth Color Shading

    glHint(GL_PERSPECTIVE_CORRECTION_HINT, GL_NICEST)
    glEnable(GL_TEXTURE_2D)

    LightAmb = (0.5, 0.5, 0.5, 1.0)
    LightDif = (1.0, 1.0, 1.0, 1.0)
    LightPos = (0.0, 0.0, 2.0, 1.0)
    # Define specular light properties
    LightSpec = [1.0, 1.0, 1.0, 1.0]

    # Assign properties to a light source
    glLightfv(GL_LIGHT0, GL_SPECULAR, LightSpec)

    # Define material properties that will interact with the light
    MaterialSpec = [1.0, 1.0, 1.0, 1.0]
    MaterialShininess = [50.0]

    glMaterialfv(GL_FRONT, GL_SPECULAR, MaterialSpec)
    glMaterialfv(GL_FRONT, GL_SHININESS, MaterialShininess)


    glLightfv(GL_LIGHT0, GL_AMBIENT, LightAmb)
    glLightfv(GL_LIGHT0, GL_DIFFUSE, LightDif)
    glLightfv(GL_LIGHT0, GL_POSITION, LightPos)
    glEnable(GL_LIGHT0)
    glEnable(GL_LIGHTING)

    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()  # Reset The Projection Matrix

    # Calculate The Aspect Ratio Of The Window
    gluPerspective(45.0, float(Width)/float(Height), 0.1, 100.0)

    glMatrixMode(GL_MODELVIEW)


# The function called when our window is resized (which shouldn't happen if you enable fullscreen, below)
def ReSizeGLScene(Width, Height):
    if Height == 0:  # Prevent A Divide By Zero If The Window Is Too Small
        Height = 1

    glViewport(0, 0, Width, Height)  # Reset The Current Viewport And Perspective Transformation
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    gluPerspective(45.0, float(Width) / float(Height), 0.1, 100.0)
    glMatrixMode(GL_MODELVIEW)

def DrawStars(Width,Height):

    glColor3f(1.0, 1.0, 1.0);
    glTexGeni(GL_S, GL_TEXTURE_GEN_MODE, GL_SPHERE_MAP)
    glTexGeni(GL_T, GL_TEXTURE_GEN_MODE, GL_SPHERE_MAP)
    glDisable(GL_DEPTH_TEST)
    
    glBindTexture( GL_TEXTURE_2D, LoadTextures('stars.bmp') )
    glPushMatrix()
    glBegin(GL_QUADS)
    glTexCoord2f(-Width,Height)
    glVertex2d(-Width,-Height)
    glTexCoord2f(Width,Width)
    glVertex2d(Width,0)
    glTexCoord2f(Width,0.0)
    glVertex2d(Width,Height)
    glTexCoord2f(0.0,0.0)
    glVertex2d(0,Height)
    glEnd()
    glPopMatrix()
    glEnable(GL_DEPTH_TEST)
    

def DrawSun():
    global Q
    glColor3f(1.0, 1.0, 1.0);
    glBindTexture( GL_TEXTURE_2D, LoadTextures('sun.tga') )
    
    Q=gluNewQuadric()
    gluQuadricNormals(Q, GL_SMOOTH)
    gluQuadricTexture(Q, GL_TRUE)
    glTexGeni(GL_S, GL_TEXTURE_GEN_MODE, GL_SPHERE_MAP)
    glTexGeni(GL_T, GL_TEXTURE_GEN_MODE, GL_SPHERE_MAP)
    
    gluSphere(Q, 0.7, 32, 16)
    
    glColor4f(1.0, 1.0, 1.0, 0.4)
    glEnable(GL_BLEND)
    glBlendFunc(GL_SRC_ALPHA, GL_ONE)
    glEnable(GL_TEXTURE_GEN_S)
    glEnable(GL_TEXTURE_GEN_T)
    gluSphere(Q, 0.7, 32, 16)

    glDisable(GL_TEXTURE_GEN_S)
    glDisable(GL_TEXTURE_GEN_T)
    glDisable(GL_BLEND)
    gluDeleteQuadric( Q )

def DrawMercury():
    global Q2
    glColor3f(1.0, 1.0, 1.0);
    glBindTexture( GL_TEXTURE_2D, LoadTextures('mercurymap.bmp') )
    
    Q2=gluNewQuadric()
    gluQuadricNormals(Q2, GL_SMOOTH)
    gluQuadricTexture(Q2, GL_TRUE)
    glTexGeni(GL_S, GL_TEXTURE_GEN_MODE, GL_SPHERE_MAP)
    glTexGeni(GL_T, GL_TEXTURE_GEN_MODE, GL_SPHERE_MAP)
    
    glPushMatrix()
    glTranslatef(0.0,0.0,1.9)			
    gluSphere(Q2,0.2,32,16) 
    glPopMatrix()
    
    gluDeleteQuadric( Q2 )

def DrawVenus():
    global Q3
    glColor3f(1.0, 1.0, 1.0);
    glBindTexture( GL_TEXTURE_2D, LoadTextures('venusmap.bmp') )
    
    Q3=gluNewQuadric()
    gluQuadricNormals(Q3, GL_SMOOTH)
    gluQuadricTexture(Q3, GL_TRUE)
    glTexGeni(GL_S, GL_TEXTURE_GEN_MODE, GL_SPHERE_MAP)
    glTexGeni(GL_T, GL_TEXTURE_GEN_MODE, GL_SPHERE_MAP)


    glPushMatrix() 
    glTranslatef(0.0,0.0,3.0)			
    gluSphere(Q3,0.3,32,16) 
    glPopMatrix()
    
    gluDeleteQuadric( Q3 )
    
    
def DrawEarth():
    global Q1
    glColor3f(1.0, 1.0, 1.0);
    glBindTexture( GL_TEXTURE_2D, LoadTextures('earthmap.bmp') )
    
    Q1=gluNewQuadric()
    gluQuadricNormals(Q1, GL_SMOOTH)
    gluQuadricTexture(Q1, GL_TRUE)
    glTexGeni(GL_S, GL_TEXTURE_GEN_MODE, GL_SPHERE_MAP)
    glTexGeni(GL_T, GL_TEXTURE_GEN_MODE, GL_SPHERE_MAP)
	
    glPushMatrix()
    glTranslatef(0.0,0.0,4.0)			
    gluSphere(Q1,0.40,32,16) 
    gluDeleteQuadric( Q1 )
    glPopMatrix()
    
def DrawMars():
    global Q4
    glColor3f(1.0, 1.0, 1.0);
    glBindTexture( GL_TEXTURE_2D, LoadTextures('marsmap.bmp') )
    
    Q4=gluNewQuadric()
    gluQuadricNormals(Q4, GL_SMOOTH)
    gluQuadricTexture(Q4, GL_TRUE)
    glTexGeni(GL_S, GL_TEXTURE_GEN_MODE, GL_SPHERE_MAP)
    glTexGeni(GL_T, GL_TEXTURE_GEN_MODE, GL_SPHERE_MAP)

    glPushMatrix()
    glTranslatef(0.0,0.0,5.5)			
    gluSphere(Q4,0.45,32,16)	
    gluDeleteQuadric( Q4 )
    glPopMatrix()

def DrawJupiter():
    global Q5
    glColor3f(1.0, 1.0, 1.0);
    glBindTexture( GL_TEXTURE_2D, LoadTextures('jupitermap.bmp') )
    
    Q5=gluNewQuadric()
    gluQuadricNormals(Q5, GL_SMOOTH)
    gluQuadricTexture(Q5, GL_TRUE)
    glTexGeni(GL_S, GL_TEXTURE_GEN_MODE, GL_SPHERE_MAP)
    glTexGeni(GL_T, GL_TEXTURE_GEN_MODE, GL_SPHERE_MAP)
    
    glPushMatrix()
    glTranslatef(0.0,0.0,7.0)			# Center The Cylinder
    gluSphere(Q5,0.60,32,16) 
    glPopMatrix()
	
    gluDeleteQuadric( Q5 )
    
def DrawSaturn():
    global Q6
    glColor3f(1.0, 1.0, 1.0);
    glBindTexture( GL_TEXTURE_2D, LoadTextures('saturnmap.bmp') )
    
    Q6=gluNewQuadric()
    gluQuadricNormals(Q6, GL_SMOOTH)
    gluQuadricTexture(Q6, GL_TRUE)
    glTexGeni(GL_S, GL_TEXTURE_GEN_MODE, GL_SPHERE_MAP)
    glTexGeni(GL_T, GL_TEXTURE_GEN_MODE, GL_SPHERE_MAP)
    
    glPushMatrix()
    glTranslatef(0.0,0.0,8.5)	
    glPushMatrix()
    glScalef(1.1,1,1)		# Center The Cylinder
    #special case to for its ring
    glutWireTorus(0.10,0.67, 100, 50);
    glPopMatrix()
    gluSphere(Q6,0.55,32,16) 
    glPopMatrix()	
    gluDeleteQuadric( Q6 )


def DrawUranus():
    global Q7
    glColor3f(1.0, 1.0, 1.0);
    glBindTexture( GL_TEXTURE_2D, LoadTextures('uranusmap.bmp') )
    
    Q7=gluNewQuadric()
    gluQuadricNormals(Q7, GL_SMOOTH)
    gluQuadricTexture(Q7, GL_TRUE)
    glTexGeni(GL_S, GL_TEXTURE_GEN_MODE, GL_SPHERE_MAP)
    glTexGeni(GL_T, GL_TEXTURE_GEN_MODE, GL_SPHERE_MAP)
    
    glPushMatrix()
    glTranslatef(0.0,0.0,10.0)			# Center The Cylinder
    gluSphere(Q7,0.55,32,16) 
    glPopMatrix()
    gluDeleteQuadric( Q7 )

def DrawNeptuno():
    global Q8
    glColor3f(1.0, 1.0, 1.0);
    glBindTexture( GL_TEXTURE_2D, LoadTextures('neptunemap.bmp') )
	
    Q8=gluNewQuadric()
    gluQuadricNormals(Q8, GL_SMOOTH)
    gluQuadricTexture(Q8, GL_TRUE)
    glTexGeni(GL_S, GL_TEXTURE_GEN_MODE, GL_SPHERE_MAP)
    glTexGeni(GL_T, GL_TEXTURE_GEN_MODE, GL_SPHERE_MAP)
    
    glPushMatrix() 
    glTranslatef(0.0,0.0,11.5)			# Center The Cylinder
    gluSphere(Q8,0.45,32,16)
    glPopMatrix()
    gluDeleteQuadric( Q8 )
    
def DrawGLScene():
    global rot, texture,rot2,rot3,rot4, rot5, rot6, rot7, rot8

    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)  # Clear The Screen And The Depth Buffer
    glLoadIdentity()  # Reset The View

    glTranslatef(0.0, 0.0, -20.0)  # Move Into The Screen

    glRotatef(rot, 1.0, 0.0, 0.0)  # Rotate The Cube On It's X Axis
    glRotatef(rot, 0.0, 1.0, 0.0)  # Rotate The Cube On Its's Y Axis
    glRotatef(-1, 0.0, 0.0, 1.0)  # Rotate The Cube On It's Z Axis
    DrawMercury()

    glRotatef(rot2, 1.0, 0.0, 0.0)  # Rotate The Cube On It's X Axis
    glRotatef(rot2, 0.0, 1.0, 0.0)  # Rotate The Cube On Its's Y Axis
    glRotatef(-1, 0.0, 0.0, 1.0)  # Rotate The Cube On It's Z Axis
    DrawVenus()

    glRotatef(rot3, 1.0, 0.0, 0.0)  # Rotate The Cube On It's X Axis
    glRotatef(rot3, 0.0, 1.0, 0.0)  # Rotate The Cube On Its's Y Axis
    glRotatef(-1, 0.0, 0.0, 1.0)  # Rotate The Cube On It's Z Axis
    DrawEarth()

    glRotatef(rot4, 1.0, 0.0, 0.0)  # Rotate The Cube On It's X Axis
    glRotatef(rot4, 0.0, 1.0, 0.0)  # Rotate The Cube On Its's Y Axis
    glRotatef(-1, 0.0, 0.0, 1.0)  # Rotate The Cube On It's Z Axis
    DrawMars()

    glRotatef(rot5, 1.0, 0.0, 0.0)  # Rotate The Cube On It's X Axis
    glRotatef(rot5, 0.0, 1.0, 0.0)  # Rotate The Cube On Its's Y Axis
    glRotatef(-1, 0.0, 0.0, 1.0)  # Rotate The Cube On It's Z Axis
    DrawJupiter()

    glRotatef(rot6, 1.0, 0.0, 0.0)  # Rotate The Cube On It's X Axis
    glRotatef(rot6, 0.0, 1.0, 0.0)  # Rotate The Cube On Its's Y Axis
    glRotatef(-1, 0.0, 0.0, 1.0)  # Rotate The Cube On It's Z Axis
    DrawSaturn()

    glRotatef(rot7, 1.0, 0.0, 0.0)  # Rotate The Cube On It's X Axis
    glRotatef(rot7, 0.0, 1.0, 0.0)  # Rotate The Cube On Its's Y Axis
    glRotatef(-1, 0.0, 0.0, 1.0)  # Rotate The Cube On It's Z Axis
    DrawUranus()

    glRotatef(rot8, 1.0, 0.0, 0.0)  # Rotate The Cube On It's X Axis
    glRotatef(rot8, 0.0, 1.0, 0.0)  # Rotate The Cube On Its's Y Axis
    glRotatef(-1, 0.0, 0.0, 1.0)  # Rotate The Cube On It's Z Axis
    DrawNeptuno()
    
    glPushMatrix()
    #DrawStars(25,25)
    glPopMatrix()
    DrawSun()  

    # Start Drawing The Cube
    rot = (rot + 0.16) % 360  
    rot2 = (rot2 + 0.14) % 360
    rot3 = (rot3 + 0.12) % 360
    rot4 = (rot3 + 0.010) % 360
    rot5 = (rot3 + 0.008) % 360
    rot6 = (rot3 + 0.006) % 360
    rot7 = (rot3 + 0.004) % 360
    rot8 = (rot8 + 0.002) % 360

    #  since this is double buffered, swap the buffers to display what just got drawn.
    glutSwapBuffers()

def main():
    global window
    global light_status

    light_status = False
    glutInit(sys.argv)

    # Select type of Display mode:
    #  Double buffer
    #  RGBA color
    # Alpha components supported
    # Depth buffer
    glutInitDisplayMode(GLUT_RGBA | GLUT_DOUBLE | GLUT_DEPTH)

    # get a 640 x 480 window
    glutInitWindowSize(612, 540)

    # the window starts at the upper left corner of the screen
    glutInitWindowPosition(0, 0)

    # Create the window with the title "Solar System"
    window = glutCreateWindow("Solar System")

    # Register the drawing function with glut, BUT in Python land, at least using PyOpenGL, we need to
    # set the function pointer and invoke a function to actually register the callback, otherwise it
    # would be very much like the C version of the code.
    glutDisplayFunc(DrawGLScene)

    # Uncomment this line to get full screen.
    #glutFullScreen()

    # When we are doing nothing, redraw the scene.
    glutIdleFunc(DrawGLScene)

    # Register the function called when our window is resized.
    glutReshapeFunc(ReSizeGLScene)

    # Register the keyboard callback so we can have keyboard interaction
    glutKeyboardFunc(keyboard)

    # Initialize our window.
    InitGL(612, 540)

    # Start Event Processing Engine
    glutMainLoop()



# Print message to console, and kick off the main to get it rolling.
if __name__ == "__main__":
    print("Hit ESC key to quit.")
    main()















