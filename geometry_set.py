#!/usr/bin/env python3

####################
### Dependencies ###
####################

import numpy as np
from collections import namedtuple

########################
### Global variables ###
########################

LINE_COLOR = "#0000FF"
POINT_SIZE = 2
POINT_COLOR = '#ffffff'

CANVAS_WIDTH = 840
CANVAS_HEIGHT = 560

OBJECT_POSITION = [CANVAS_WIDTH//2, CANVAS_HEIGHT-20]
OBJECT_SCALE = 2500

Angle = namedtuple('Angle', 'x y z')

def UpdatePosition(x, y):
    global OBJECT_POSITION

    OBJECT_POSITION[0] += x
    OBJECT_POSITION[1] += y

def DrawFace(face, points, canvas):
    ''' Draw a specified face. '''
    draw_points = []
    for index in face:
        draw_points.extend(points[index-1])
    canvas.create_polygon(draw_points, outline=LINE_COLOR, fill='')

def DrawPoint(point, canvas):
    canvas.create_line(*point, *point, width=POINT_SIZE, fill=POINT_COLOR)

def RotationMatrix(angles_xyz):
    #These are the rotation matricies that will transform the point position
    #according to the desired rotation (Check some linear algebra course
    #if you wanna know more about em, otherwise, there's no huge need
    #to understand exactly how they work)

    cos = Angle(*(np.cos(angle) for angle in angles_xyz))
    sin = Angle(*(np.sin(angle) for angle in angles_xyz))

    rot_x = np.array([[1, 0    , 0     ],
                      [0, cos.x, -sin.x],
                      [0, sin.x, cos.x ]])

    rot_y = np.array([[cos.y, 0, -sin.y],
                      [0    , 1, 0     ],
                      [sin.y, 0, cos.y ]])

    rot_z = np.array([[cos.z, -sin.z, 0],
                      [sin.z, cos.z , 0],
                      [0    , 0     , 1]])

    return rot_z @ rot_x @ rot_y

#This function is the one that orchestrates all the actions.
#First is transforms the points, draws them, then draws the lines
#according to the faces list
def DrawObject(canvas, vertices, Faces, angles_xyz, zoom):
    # only calculate this once, since it's the same for all the points
    rotation = RotationMatrix(angles_xyz)
    # vectorised matrix arithmetic - do them all at once
    rotated = rotation @ vertices
    point_scales = OBJECT_SCALE / (zoom - rotated[2])

    projected_points = (rotated[:2] * [[1],[-1]] * point_scales).T \
                      + OBJECT_POSITION
    for point in projected_points:
        DrawPoint(point, canvas)

    for face in Faces:
        DrawFace(face, projected_points, canvas)
    return canvas

if __name__ == '__main__':
    print("""This is not the executable file,
             go to the 'main.py' file and run
             it instead!""")
