#!/usr/bin/env python3

####################
### Dependencies ###
####################

import math
import gc
import numpy as np

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

def RotationMatrix(angle_x, angle_y, angle_z):
    #These are the rotation matricies that will transform the point position
    #according to the desired rotation (Check some linear algebra course
    #if you wanna know more about em, otherwise, there's no huge need
    #to understand exactly how they work)
    rot_x = np.array([[1, 0, 0],
                      [0, math.cos(angle_x), -math.sin(angle_x)],
                      [0, math.sin(angle_x), math.cos(angle_x)]])

    rot_y = np.array([[math.cos(angle_y), 0, -math.sin(angle_y)],
                      [0, 1, 0],
                      [math.sin(angle_y), 0, math.cos(angle_y)]])

    rot_z = np.array([[math.cos(angle_z), -math.sin(angle_z), 0],
                      [math.sin(angle_z), math.cos(angle_z), 0],
                      [0, 0 ,1]])
    return rot_z @ rot_x @ rot_y

#This function is the one that orchestrates all the actions.
#First is transforms the points, draws them, then draws the lines
#according to the faces list
def DrawObject(canvas, vertices, Faces, angle_x, angle_y, angle_z, zoom):
    projected_points = []
    # only calculate this once, since it's the same for all the points
    rotation = RotationMatrix(angle_x, angle_y, angle_z)
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
