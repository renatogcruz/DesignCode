"""
Drawing a simple trellis.
Environment - rhinoceros + grasshopper
Language    - python

What is a simple trellis?
In structural engineering, a lattice is a structure composed 
of triangular units constructed with straight elements whose 
ends are connected at points known as knots. External forces 
and reactions are considered, in a simplified way, applied in 
these same nodes.

INPUTS
spacing  - Item acess {type him = ghdoc rhinoscriptsintax};
zNum     - Item acess {type him = ghdoc rhinoscriptsintax};
yNum     - Item acess {type him = ghdoc rhinoscriptsintax}.
OUTPUTS
out      - the execution information;
bars     - output bars {boxes};
braces   - outputs braces {diagonals};
supports - outputs supports {point of connections};
load     - outputs load {point of load}.

Reference - Danil NAGY
"""

import Rhino.Geometry as rh

points = []

for y in range(int(yNum+1)):
    points.append([])
    for z in range(int(zNum+1)):
        points[-1].append(rh.Point3d(0, y*spacing, z*spacing))

bars = []
braces = []

for i in range(len(points)):
    for j in range(len(points[i])):
        if i < len(points) - 1:
            bars.append(rh.Line(points[i][j], points[i+1][j]))
        
        if j < len(points[i]) - 1:
            bars.append(rh.Line(points[i][j], points[i][j+1]))
        
        if i < len(points) - 1 and j < len(points[i]) - 1:
            braces.append(rh.Line(points[i][j], points[i+1][j+1]))
        
        if i > 0 and j < len(points[i]) - 1:
            braces.append(rh.Line(points[i][j], points[i-1][j+1]))

supports = points[:][0]
load = points[-1][-1]