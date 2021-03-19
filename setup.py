# setup.py
# Tawfeeq Mannan
# Last updated 2021/03/18

# imports
from math import sqrt
from Celestial import Celestial


# help text
helpMsg = """\
    --------------------------------------------------
    1 | The Earth, the Moon, two satellites in Earth orbit, \
and a satellite in lunar orbit.
    2 | A central body slowly moving to the right, with \
two smaller bodies in orbit around it.
    3 | Three bodies in a chaotic orbit with no pattern.
    4 | Two large bodies orbiting in a large circle, \
disturbing the orbits of two smaller bodies within.
    5 | Two binary stars with two small masses \
falling towards them and getting flung around.
    6 | Identical bodies crashing to test collision simulation.
    --|-----------------------------------------------
    0 | Create a custom system of your own!
    --------------------------------------------------
"""


# function definitions
def getCelestials():
    # get number of celestials in system
    n = 0
    while True:
        try:
            n = int(input("Enter the number of bodies in the system: "))
            if n < 0:
                raise ValueError
            print()
            break
        except ValueError:
            print("Please enter a positive number of celestial bodies.\n")
    
    # use previous input to get info for each celestial and whether static
    c, s = [], []
    for i in range(n):
        print("Enter details for object #" + str(i + 1) + ":")
        while True:
            try:
                x = float(input("x coordinate: "))
                y = float(input("y coordinate: "))
                vx = float(input("x-component of velocity: "))
                vy = float(input("y-component of velocity: "))
                Gm = float(input("Gravitational parameter: "))
                if Gm < 0:
                    raise IndexError
                r = float(input("Size (radius) of the body: "))
                if r < 0:
                    raise IndexError

                static = input("Immovable body? (y/n): ")
                if static.lower().startswith('y'):
                    static = True
                else:
                    static = False

                c.append(Celestial(x, y, vx, vy, Gm, r))
                if static:
                    s.append(i)
                print()
                break
            except ValueError:
                print("Please enter numbers only.\n")
            except IndexError:
                print("Please use positive numbers only for GM or R.\n")
    
    return c, s


# list definitions
allCelestials = [
    # earth, moon, lunar satellite, and two earth satellites.
    [
        Celestial(100000, 0, 0, 2, 0, 0),
        Celestial(230000, 0, 0, 1.33, 0, 0),
        Celestial(370000, 0, 0, 1.6, 0, 0),
        Celestial(384400, 0, 0, 1.0183, 4900, 1737),
        Celestial(0, 0, 0, 0, 398600, 6371),
    ],


    # three bodies creeping to the right.
    #     former two orbit the latter.
    [
        Celestial(-500000, -150000, 1.55, 0, 1000, 500),
        Celestial(-500000, 50000, -2.3, 0, 10000, 1000),
        Celestial(-500000, 0, 0.2, 0, 300000, 5000),
    ],


    # three bodies in chaotic but non-colliding orbit.
    [
        Celestial(300000, 0, 0, 0.2, 2500, 500),
        Celestial(100000, -50000, 0, 0.1, 5000, 1000),
        Celestial(-100000, 50000, 0, -0.1, 10000, 5000),
    ],


    # four bodies in chaotic orbit with radial symmetry.
    #     first object throws the orbits out of balance.
    [
        # Celestial(0, 500000, 0, 0, 100),
        Celestial(-50000, 50000, 0, -0.073, 2500, 1000),
        Celestial(50000, -50000, 0, 0.073, 2500, 1000),
        Celestial(400000, 0, 0, 0.13, 10000, 5000),
        Celestial(-400000, 0, 0, -0.13, 10000, 5000),
    ],

    # two binary "stars" with two small masses in chaotic fall
    [
        Celestial(500000, 0, 0, 0, 1000, 1000),
        Celestial(-500000, 0, 0, 0, 1000, 1000),
        Celestial(200000, 0, 0, 0.35, 100000, 5000),
        Celestial(-200000, 0, 0, -0.35, 100000, 5000),
    ],

    # elastic collision test
    [
        Celestial(0, 0, 0, 0, 500000, 10000),
        Celestial(500000, 0, -2, 0, 500000, 10000),
    ],
]

allStaticBodies = [
    [4],
    [],
    [],
    [],
    [],
    [],
]
