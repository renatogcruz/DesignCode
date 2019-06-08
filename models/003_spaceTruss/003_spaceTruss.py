"""
Drawing a space truss
Environment - rhinoceros + grasshopper
Language    - python

What is a space truss?
See here: https://en.wikipedia.org/wiki/Space_frame

INPUTS
side        - Item acess {type hint = float};
index       - Item acess {type hint = int};
xNum        - Item acess {type hint = int};
yNum        - Item acess {type hint = int};
height      - Item acess {type hint = float};

OUTPUTS
out         - the execution information;
                            0 - Side dimension: {float}
                            1 - Number of modules: {int/unit}
                            2 - Modular dimensions: {float}
upper       - outputs upper  bars;
below       - outputs below bars;
diagonal    - outputs diagonals bars;
support     - outputs support points;
a           - outputs upper points.

Autor - Renato Godoi da Cruz
email - renatogcruz@hotmail.com
"""

import Rhino.Geometry as rh

#size [variable] * num [variable] == side [immutable]
x = side / index
a = side
size = x

#points
points = []
#carga = []   #PROVISÓRIO

for y in range (int(yNum + 1)):
    points.append ([])
    for x in range (int(xNum +1)):
        points[-1].append (rh.Point3d(x * size,y * size, height))
#        carga.append((x * size,y * size, height)) #PROVISÓRIO adiciona pontos de cargas

points2 = []

for y in range (int(yNum)):
    points2.append ([])
    for x in range (int(xNum)):
        points2[-1].append (rh.Point3d(x * size + size/2, y * size + size/2, 0))

below = []

for i in range(len(points2)):         
    for j in range(len(points2[i])):  
        if i < len(points2) - 1:
            below.append(rh.Line(points2[i][j], points2[i+1][j]))
        if j < len(points2[i]) - 1:
            below.append(rh.Line(points2[i][j], points2[i][j+1]))

upper = []     

for i in range(len(points)):         
    for j in range(len(points[i])):  
        if i < len(points) - 1:
            upper.append(rh.Line(points[i][j], points[i+1][j]))
        if j < len(points[i]) - 1:
            upper.append(rh.Line(points[i][j], points[i][j+1]))

diagonal = []

for i in range (len(points2)):
    for j in range (len(points)):
        if i < len(points2) and j < len(points) -1 : 
            diagonal.append(rh.Line(points2[i][j], points[i][j]))

        if i >= 0 and j < len(points)-1 : 
            diagonal.append(rh.Line(points2[i][j], points[i+1][j]))

        if i < len(points2) and j < len(points)-1: 
            diagonal.append(rh.Line(points2[i][j], points[i][j+1]))

        if i >= 0 and j < len(points)-1 : 
            diagonal.append(rh.Line(points2[i][j], points[i+1][j+1]))


support = (points2[0][0], points2 [0][-1], points2[-1][0], points2[-1][-1])

a = points

print ('Side dimension: %.2f m' %(size * xNum))
numModules = index * index
print ('Number of modules: %s unid.' %numModules)
print ('Modular dimensions: %.2f m' %x)