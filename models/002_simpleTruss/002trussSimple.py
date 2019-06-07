"""
Drawing a simple truss
Environment - rhinoceros + grasshopper
Language    - python

What is a simple truss?
In structural engineering, a lattice is a structure composed 
of triangular units constructed with straight elements whose 
ends are connected at points known as knots. External forces 
and reactions are considered, in a simplified way, applied in 
these same nodes.

INPUTS
length         - Item acess {type him = ghdoc rhinoscriptsintax};
                             receive float
height         - Item acess {type him = ghdoc rhinoscriptsintax};
segments       - Item acess {type him = ghdoc rhinoscriptsintax};
slope          - Item acess {type him = ghdoc rhinoscriptsintax};
edge_diagonais - Item acess {type him = ghdoc rhinoscriptsintax};
truss_type     - Item acess {type him = ghdoc rhinoscriptsintax}.
                             - Options:
                                 Warren;
                                 Warren Flipped;
                                 Howe;
                                 Pratt.

OUTPUTS
out            - the execution information;
pt_top         - outputs top points;
pt_bot         - outputs bot points;
diagonals      - outputs braces {diagonals};
bot_ch         - outputs {banzo inferior};
top_ch         - outputs {banzo superior};
vert           - outputs {montante}.

Reference - Daniel C.
"""

import rhinoscriptsyntax as rs
import math

print("Simple TRUSS 002")

#start point & end point of truss
start = 0,0,0
end = (length, 0,0)
pt1 = rs.coerce3dpoint(start)
pt2 = rs.coerce3dpoint(end)

#calculation of span length & division count & segment length = length increment
span = rs.Distance(pt1, pt2)
segments = int(segments)
length_increment = span/segments

#slope calculation from percentage to degrees
slope_perc = slope
slope_ang = math.atan(slope/100)

#calculation of height increment
height_increment = (span/segments)*math.tan(slope_ang)
n = height
height_step = height_increment
length_step = length_increment

#empty variables
a = []
b = []
c = []
d = []
e = []

#slope calculation
slope_perc = slope
slope_ang = math.atan(slope/100)

#generation of bot chord points
j = 0
for i in range(segments+1):
    j = j + length_step
    bot = rs.AddPoint(j-length_step,0,0)
    b.append(bot)

#generation of top chord points
j = 0
for i in range(segments+1):
#    print (n)
    if i <= segments/2:
        n = n + height_step
        j = j + length_step
        top = rs.AddPoint(j - length_step,0,n - height_step)
    else:
        n = n - height_step
        top = rs.AddPoint(j,0,n - height_step)
        j = j + length_step
    a.append(top)

#assigning variables
pt_top = a
pt_bot = b

#generation of diagonals_1
j = 0
for i in range(segments):
    diagonal = rs.AddLine(pt_bot[j],pt_top[j+1])
    j = j + 1
    c.append(diagonal)

#generation of diagonals_2
j = 0
for i in range(segments):
    diagonal = rs.AddLine(pt_bot[j+1],pt_top[j])
    j = j + 1
    d.append(diagonal)

#generation of bottom chord and top chords
bot_ch = rs.AddLine(pt_bot[0],pt_bot[segments])
top_ch = [rs.AddLine(pt_top[0],pt_top[int(segments/2)]), rs.AddLine(pt_top[int(segments/2)],pt_top[segments])]

#generation of verticals
j = 0
for i in range(segments+1):
    vertical = rs.AddLine(pt_bot[j],pt_top[j])
    j = j + 1
    e.append(vertical)

#assigning variables
dia_1 = c
dia_2 = d
vert = e

#Warren
if truss_type == 0:
    if segments/2 % 2 == 1:
        diagonals = dia_2[slice(1, int(segments/2),2)] + dia_1[slice(int(segments/2+1), int(segments),2)]
        diagonals = dia_1[slice(0, int(segments/2),2)] + dia_2[slice(int(segments/2), int(segments),2)]
    else:
        diagonals = dia_2[slice(1, int(segments/2),2)] + dia_1[slice(int(segments/2), int(segments),2)]
        diagonals = dia_1[slice(0, int(segments/2),2)] + dia_2[slice(int(segments/2+1), int(segments),2)]
#Warren Flipped
if truss_type == 1:
    if segments/2 % 2 == 1:
        diagonals = dia_2[slice(0, int(segments/2),2)] + dia_1[slice(int(segments/2), int(segments),2)]
        diagonals = dia_1[slice(1, int(segments/2),2)] + dia_2[slice(int(segments/2+1), int(segments),2)]
    else:
        diagonals = dia_2[slice(0, int(segments/2),2)] + dia_1[slice(int(segments/2+1), int(segments),2)]
        diagonals = dia_1[slice(1, int(segments/2),2)] + dia_2[slice(int(segments/2), int(segments),2)]
#Howe
if truss_type == 2:
    if edge_diagonals < segments/2:
        diagonals = dia_1[slice(0, int(edge_diagonals))] + dia_2[slice(int(segments-edge_diagonals), int(segments))]
        diagonals = dia_1[slice(int(edge_diagonals), int(segments/2))] + dia_2[slice(int(segments/2), int(segments-edge_diagonals))]
    else:
        diagonals = dia_1[slice(0, int(segments/2))] + dia_2[slice(int(segments/2), int(segments))]
        diagonals = []
#Pratt
if truss_type == 3:
    if edge_diagonals < segments/2:
        diagonals = dia_2[slice(0, int(edge_diagonals))] + dia_1[slice(int(segments-edge_diagonals), int(segments))]
        diagonals = dia_2[slice(int(edge_diagonals), int(segments/2))] + dia_1[slice(int(segments/2), int(segments-edge_diagonals))]
    else:
        diagonals = dia_2[slice(0, int(segments/2))] + dia_1[slice(int(segments/2), int(segments))]
        diagonals = []