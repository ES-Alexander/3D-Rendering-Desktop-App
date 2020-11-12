#! /usr/bin/env python3

import re
import numpy as np

def ExtractData(file):
    vertices = []
    faces = []

    #Read more about how waveform (.obj) files are structured to understand
    #how this code exactly works, but shortly:
    #   *If the line starts with a "v", then that's a vertex and what follows is
    #   its X, Y, Z coordinates (foats)
    #   *If the line starts with a "f", then that's a face and what follows is
    #   the list of vertices to be connected to create a face
    #   (formatted a bit strangely though, I recommend checking an example)
    for line in file.readlines():
        if line[0:2] == "v ":
            vertices.append([float(x) for x in re.findall("[-+]?[.]?[\d]+(?:,\d\d\d)*[\.]?\d*(?:[eE][-+]?\d+)?", line)])
        elif line[0:2] == "f ":
            faces.append([int(vertex.split("/")[0]) for vertex in line[2:-2].split(' ')])
    return np.array(vertices).T, faces


if __name__ == '__main__':
    print("""This is not the executable file,
             go to the 'main.py' file and run
             it instead!""")
