#! /usr/bin/env python3

import numpy as np

# .obj format specifications
OBJ_VERTEX = 'v'
OBJ_FACE   = 'f'

def ExtractData(file):
    #Read more about how waveform (.obj) files are structured to understand
    #how this code exactly works, but shortly:
    #   *If the line starts with a "v", then that's a vertex and what follows is
    #   its X, Y, Z coordinates (foats)
    #   *If the line starts with a "f", then that's a face and what follows is
    #   the list of vertices to be connected to create a face
    #   (formatted a bit strangely though, I recommend checking an example)

    # start with no vertices or faces
    vertices = []
    faces = []
    relevants = [relevant + ' ' for relevant in (OBJ_VERTEX, OBJ_FACE)]

    # populate them from the file
    for line in file:
        # use a generator to stop checking early if possible
        if all(not line.startswith(relevant) for relevant in relevants):
            continue # ignore all lines that aren't relevant
        data = line.split()
        line_type = data[0]
        data = data[1:]
        if line_type == OBJ_VERTEX:
            vertices.append([float(x) for x in data])
        elif line_type == OBJ_FACE:
            # only get the vertex index, not texture or normal
            faces.append([int(f.split('/')[0]) for f in data])
        # ignore all other types of data in the file
    return np.array(vertices).T, faces


if __name__ == '__main__':
    print("""This is not the executable file,
             go to the 'main.py' file and run
             it instead!""")
