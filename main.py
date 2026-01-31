from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *
import sys

angle = 0.0
win_width, win_height = 1920, 1080
import math

yaw, pitch = 0.0, 0.0
# forward vector
dir_x = math.sin(math.radians(yaw))
dir_z = -math.cos(math.radians(yaw))

speed = 0.1  # camera movement speed

def draw_cube(x,y,z,color,scale_x,scale_y,scale_z):
        glBegin(GL_QUADS)
         # Front
        glColor3f(*color)
        glNormal3f(0, 0, 1)
        glVertex3f(x - 0.5 * scale_x, y - 0.5 * scale_y, z + 0.5 * scale_z)
        glVertex3f(x + 0.5 * scale_x, y - 0.5 * scale_y, z + 0.5 * scale_z)
        glVertex3f(x + 0.5 * scale_x, y + 0.5 * scale_y, z + 0.5 * scale_z)
        glVertex3f(x - 0.5 * scale_x, y + 0.5 * scale_y, z + 0.5 * scale_z)

        # Back
        glNormal3f(0, 0, -1)
        glVertex3f(x - 0.5 * scale_x, y - 0.5 * scale_y, z - 0.5 * scale_z)
        glVertex3f(x - 0.5 * scale_x, y + 0.5 * scale_y, z - 0.5 * scale_z)
        glVertex3f(x + 0.5 * scale_x, y + 0.5 * scale_y, z - 0.5 * scale_z)
        glVertex3f(x + 0.5 * scale_x, y - 0.5 * scale_y, z - 0.5 * scale_z)

        # Left
        glNormal3f(-1, 0, 0)
        glVertex3f(x - 0.5 * scale_x, y - 0.5 * scale_y, z - 0.5 * scale_z)
        glVertex3f(x - 0.5 * scale_x, y - 0.5 * scale_y, z + 0.5 * scale_z)
        glVertex3f(x - 0.5 * scale_x, y + 0.5 * scale_y, z + 0.5 * scale_z)
        glVertex3f(x - 0.5 * scale_x, y + 0.5 * scale_y, z - 0.5 * scale_z)

        # Right
        glNormal3f(1, 0, 0)
        glVertex3f(x + 0.5 * scale_x, y - 0.5 * scale_y, z - 0.5 * scale_z)
        glVertex3f(x + 0.5 * scale_x, y + 0.5 * scale_y, z - 0.5 * scale_z)
        glVertex3f(x + 0.5 * scale_x, y + 0.5 * scale_y, z + 0.5 * scale_z)
        glVertex3f(x + 0.5 * scale_x, y - 0.5 * scale_y, z + 0.5 * scale_z)

        # Top
        glNormal3f(0, 1, 0)
        glVertex3f(x - 0.5 * scale_x, y + 0.5 * scale_y, z - 0.5 * scale_z)
        glVertex3f(x - 0.5 * scale_x, y + 0.5 * scale_y, z + 0.5 * scale_z)
        glVertex3f(x + 0.5 * scale_x, y + 0.5 * scale_y, z + 0.5 * scale_z)
        glVertex3f(x + 0.5 * scale_x, y + 0.5 * scale_y, z - 0.5 * scale_z)

        # Bottom
        glNormal3f(0, -1, 0)
        glVertex3f(x - 0.5 * scale_x, y - 0.5 * scale_y, z - 0.5 * scale_z)
        glVertex3f(x + 0.5 * scale_x, y - 0.5 * scale_y, z - 0.5 * scale_z)
        glVertex3f(x + 0.5 * scale_x, y - 0.5 * scale_y, z + 0.5 * scale_z)
        glVertex3f(x - 0.5 * scale_x, y - 0.5 * scale_y, z + 0.5 * scale_z)

        glEnd()

def draw_sphere(pos,color):
    glPushMatrix()
    glTranslatef(*pos)  # position at origin
    glColor3f(*color)  # red color
    glutSolidSphere(1.0, 32, 32)  # radius=1, smooth
    glPopMatrix()
def draw_cylinder(pos, base_radius=1.0, top_radius=1.0, height=2.0, slices=32, stacks=1):
    quad = gluNewQuadric()

    glPushMatrix()
    glTranslatef(*pos)  # move to position
    glColor3f(1, 0, 0)  # optional color
    gluCylinder(quad, base_radius, top_radius, height, slices, stacks)
    glPopMatrix()

def mouse_motion(x, y):
    global yaw, pitch, last_x, last_y
    dx = x - last_x
    dy = y - last_y

    sensitivity = 0.2
    yaw += dx * sensitivity
    pitch -= dy * sensitivity
    pitch = max(-89, min(89, pitch))  # clamp pitch

    last_x, last_y = x, y
    glutWarpPointer(win_width // 2, win_height // 2)
    last_x, last_y = win_width // 2, win_height // 2
cam_x, cam_y, cam_z = 0.0, 0.0, 1.0


def init_camera():
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    gluPerspective(45.0, win_width / win_height, 0.1, 50.0)  # FOV, aspect, near, far
    glMatrixMode(GL_MODELVIEW)
def camera():
    global cam_x, cam_y, cam_z, yaw, pitch
    glLoadIdentity()

    # Calculate front vector
    front_x = math.cos(math.radians(pitch)) * math.sin(math.radians(yaw))
    front_y = math.sin(math.radians(pitch))
    front_z = -math.cos(math.radians(pitch)) * math.cos(math.radians(yaw))

    # Target = camera + front
    target_x = cam_x + front_x
    target_y = cam_y + front_y
    target_z = cam_z + front_z

    gluLookAt(cam_x, cam_y, cam_z, target_x, target_y, target_z, 0, 1, 0)


def controls(key, x, y):
    global cam_x, cam_y, cam_z, yaw, pitch

    # forward vector
    forward_x = math.cos(math.radians(pitch)) * math.sin(math.radians(yaw))
    forward_y = math.sin(math.radians(pitch))
    forward_z = -math.cos(math.radians(pitch)) * math.cos(math.radians(yaw))

    # right vector (XZ plane)
    right_x = math.sin(math.radians(yaw - 90))
    right_z = -math.cos(math.radians(yaw - 90))

    if key == b'w':
        cam_x += forward_x * speed
        cam_y += forward_y * speed
        cam_z += forward_z * speed
    if key == b's':
        cam_x -= forward_x * speed
        cam_y -= forward_y * speed
        cam_z -= forward_z * speed
    if key == b'd':
        cam_x -= right_x * speed
        cam_z -= right_z * speed
    if key == b'a':
        cam_x += right_x * speed
        cam_z += right_z * speed

def draw():
    global angle

    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    camera()
    # rotation

    # solid cube
    draw_cube(0, 0, 0, (0,1,0), 1.2, 1, 1)
    draw_cube(0, -1, 0, (0, 1, 0), 30, 1, 30)
    draw_sphere((10,10,10),(1,1,1))
    draw_cylinder((2,1,1))
    #draw_cube(2, -2, 0,color=(0.25,1.1,0))

    glutSwapBuffers()



def idle():
    glutPostRedisplay()

glutInit(sys.argv)
glutInitDisplayMode(GLUT_DOUBLE | GLUT_RGB | GLUT_DEPTH)
glutInitWindowSize(win_width, win_height)
glutCreateWindow(b"Colored Cube")

glEnable(GL_LIGHTING)      # enable lighting
glEnable(GL_LIGHT0)        # enable light source 0
glEnable(GL_COLOR_MATERIAL)  # let glColor affect material
glColorMaterial(GL_FRONT_AND_BACK, GL_AMBIENT_AND_DIFFUSE)
glShadeModel(GL_SMOOTH)

glEnable(GL_DEPTH_TEST)
last_x, last_y = 250, 250
glutDisplayFunc(draw)
glutIdleFunc(idle)
glutKeyboardFunc(controls)
init_camera()
glutPassiveMotionFunc(mouse_motion)
glutSetCursor(GLUT_CURSOR_NONE) # hide cursor

# Light position and color
glLightfv(GL_LIGHT0, GL_POSITION, [5.0, 5.0, 5.0, 1.0])  # x,y,z,1=positional
glLightfv(GL_LIGHT0, GL_DIFFUSE, [1.0, 1.0, 1.0, 1.0])   # diffuse color
glLightfv(GL_LIGHT0, GL_SPECULAR, [1.0, 1.0, 1.0, 1.0])  # specular color

glutMainLoop()

