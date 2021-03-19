# main.py
# Tawfeeq Mannan

# imports
import matplotlib.pyplot as plt
from matplotlib.colors import LinearSegmentedColormap
from Celestial import Celestial


# function definitions
def trimLists(trimAmount, *lists):
    for lst in lists:
        lst[:] = lst[::trimAmount]


# object declaration/instantiation
celestials = [
    # Celestial(398600, 0, 0, 0, 0),  # earth
    # Celestial(4900, 384400, 0, 0, sqrt(398600 / 384400)),  # moon
    # Celestial(0, 370000, 0, 0, 1.6),
    # Celestial(0, 230000, 0, 0, 1.33),

    # Celestial(-500000, -150000, 1.55, 0, 1000, 500),
    # Celestial(-500000, 50000, -2.3, 0, 10000, 1000),
    # Celestial(-500000, 0, 0.2, 0, 300000, 10000),

    # Celestial(300000, 0, 0, 0.2, 2500, 2500),
    # Celestial(100000, -50000, 0, 0.1, 5000, 5000),
    # Celestial(-100000, 50000, 0, -0.1, 10000, 10000),

    Celestial(0, 500000, 0, 0, 100, 0),
    Celestial(-50000, 50000, 0, -0.073, 2500, 2500),
    Celestial(50000, -50000, 0, 0.073, 2500, 2500),
    Celestial(400000, 0, 0, 0.13, 10000, 10000),
    Celestial(-400000, 0, 0, -0.13, 10000, 10000),
]

# time control variables
t = 0
DAYS = 120
T_TOTAL = DAYS * 24 * 3600
T_STEP = 60
TRIM = 20


# motion execution
collision = False
while t <= T_TOTAL:
    for i in range(len(celestials)):
        # if i == 0:
            # continue  # do not move Earth
        otherMasses = [c for j, c in enumerate(celestials) if \
            j != i and c.mu != 0]
        if not celestials[i].move(otherMasses, T_STEP):
            collision = True
            break
    
    if collision:
        print("Collision detected at", t, "seconds")
        print('(', t // 3600 // 24, 'days )')
        break
    t += T_STEP

for c in celestials:
    trimLists(TRIM, c.x, c.y, c.vx, c.vy)


# plotting
fig = plt.figure()
fig.suptitle("Positions of " + str(len(celestials)) + \
    " celestial bodies every " + str(TRIM) + " minutes over the course of " + \
        str(t // 3600 // 24) + " days")

ax = fig.add_subplot(111)

ax.axis([-800000, 800000, -500000, 500000])
ax.grid(b=True, which="major")
ax.grid(b=True, which="minor", alpha=0.2)
ax.minorticks_on()
ax.set_axisbelow(True)

ax.set(xlabel="Distance across x-axis (km)", \
    ylabel="Distance across y-axis (km)")

for c in celestials:
    dotSize = c.r / 10000 if c.r != 0 else 0.1
    ax.scatter(c.x, c.y, s=dotSize, c=range(len(c.x)), cmap="cool")
    ax.annotate(celestials.index(c) + 1, (c.x[-1], c.y[-1]), \
        xytext=(c.x[-1] + 20000, c.y[-1] + 20000), \
        arrowprops={"arrowstyle": "->"}, color="green", weight="bold")
# ax.scatter(celestials[0].x, celestials[0].y, s=20)  # Earth
# ax.scatter(celestials[1].x, celestials[1].y, s=1, \
    # c=range(len(celestials[1].x)), cmap='cool')  # Moon

fig.subplots_adjust(left=0.125, right=0.875, top=0.95, bottom=0.05)
plt.show()
