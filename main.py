# import libraries
import matplotlib.pyplot as plot
from matplotlib.colors import LinearSegmentedColormap
from math import sqrt, sin, cos, atan, pi

# immutable values
M1 = 398600
M2 = 4900
x1 = [0]
y1 = [0]
R = 384400
OMEGA = sqrt(M1 / (R ** 3))

DAYS = 116  # total time to simulate for (days)
T_STEP = 60  # integration step size (seconds)
T_TOTAL = DAYS * 24 * 3600
TRIM = 60 # trim every how many data points


# variables
def resetToInitialConditions():
    global t, theta, x2, y2, x3, y3, rx3, ry3, vx, vy
    t = 0
    theta = 0

    x2 = [R * cos(theta)]
    y2 = [R * sin(theta)]

    x3 = [230000]
    y3 = [0]
    rx3 = [x3[0]]
    ry3 = [y3[0]]
    vx = 0
    vy = 1.3

resetToInitialConditions()


# initialize matplotlib subplots (1x2, labels, axes, gridlines)
fig, axs = plot.subplots(nrows=1, ncols=2, sharex=True, sharey=True)
fig.suptitle('Position of a satellite every hour as it moves through ' + \
    'high Earth orbit in the lunar plane over a span of ' + str(DAYS) + \
        ' days \nr = ' + str(x3[-1]) + ' km \nv = ' + \
            str(vy) + ' km/s')
axs[0].set_title('Motion of satellite in inertial reference frame')
axs[1].set_title('Motion of satellite in rotating reference frame')
for ax in axs:
    ax.set(xlabel='Distance along x-axis (km)', \
        ylabel='Distance along y-axis (km)')
    ax.label_outer()
    ax.axis([-400000, 400000, -450000, 450000])
    ax.grid(b=True, which='major')
    ax.grid(b=True, which='minor', alpha=0.2)
    ax.minorticks_on()
    ax.set_axisbelow(True)


# integration functions
def moveMoonInInertialFrame():
    global R, OMEGA, T_STEP, theta, x2, y2
    theta += OMEGA * T_STEP
    x2.append(R * cos(theta))
    y2.append(R * sin(theta))

    # return true if Moon has completed sidereal revolution
    return y2[-1] > 0 and y2[-2] < 0


def moveSatelliteInInertialFrame():
    global M1, M2, x1, y1, T_STEP, x2, y2, x3, y3, vx, vy
    ax = - (M1 * (x3[-1] - x1[-1])) \
        / ((x3[-1] - x1[-1]) ** 2 + (y3[-1] - y1[-1]) ** 2) ** (3 / 2) \
            - (M2 * (x3[-1] - x2[-1])) \
                / ((x3[-1] - x2[-1]) ** 2 + (y3[-1] - y2[-1]) ** 2) ** (3 / 2)
    
    ay = - (M1 * (y3[-1] - y1[-1])) \
        / ((x3[-1] - x1[-1]) ** 2 + (y3[-1] - y1[-1]) ** 2) ** (3 / 2) \
            - (M2 * (y3[-1] - y2[-1])) \
                / ((x3[-1] - x2[-1]) ** 2 + (y3[-1] - y2[-1]) ** 2) ** (3 / 2)
    
    vx += ax * T_STEP
    vy += ay * T_STEP
    x3.append(x3[-1] + vx * T_STEP)
    y3.append(y3[-1] + vy * T_STEP)

    # return true if satellite has completed sidereal revolution
    return y3[-1] > 0 and y3[-2] < 0


def recordSatelliteInRotatingFrame():
    global x1, y1, theta, x3, y3, rx3, ry3
    dist = sqrt((x3[-1] - x1[-1]) ** 2 + (y3[-1] - y1[-1]) ** 2)
    angle = atan((y3[-1] - y1[-1]) / (x3[-1] - x1[-1]))
    if x3[-1] - x1[-1] < 0 and y3[-1] - y1[-1] > 0:
        angle += pi  # convert from Q4 to Q2
    elif x3[-1] - x1[-1] < 0 and y3[-1] - y1[-1] < 0:
        angle += pi  # convert from Q1 to Q3
    
    dTheta = angle - theta
    rx3.append(dist * cos(dTheta))
    ry3.append(dist * sin(dTheta))


# function to reduce the number of data points to clean up the scatter plot
def trimLists(trimAmount, *lists):
    for lst in lists:
        lst[:] = lst[::trimAmount]


# execution of satellite motion
while t <= T_TOTAL:
    moveMoonInInertialFrame()
    if moveSatelliteInInertialFrame():
        print("Satellite crossed x-axis at", t, "seconds.")
    recordSatelliteInRotatingFrame()
    t += T_STEP

# slimming down the data
trimLists(TRIM, x2, y2, x3, y3, rx3, ry3)


# defining colormaps to fade the satellite path history
redFadeDict = {
    'red': [(0, 1, 1), (1, 1, 1)],
    'green': [(0, 0.8, 0.8), (0.5, 0.5, 0.5), (0.9, 0.2, 0.2), (1, 0, 0)],
    'blue': [(0, 0.8, 0.8), (0.5, 0.5, 0.5), (0.9, 0.2, 0.2), (1, 0, 0)]
}
blackFadeDict = {
    'red': [(0, 0.9, 0.9), (0.8, 0.5, 0.5), (1, 0, 0)],
    'green': [(0, 0.9, 0.9), (0.8, 0.5, 0.5), (1, 0, 0)],
    'blue': [(0, 0.9, 0.9), (0.8, 0.5, 0.5), (1, 0, 0)]
}
redFade = LinearSegmentedColormap('', redFadeDict)
blackFade = LinearSegmentedColormap('', blackFadeDict)


# plot the Earth, Moon, and satellite in inertial frame
axs[0].scatter(x1, y1, s=30, c='blue')
axs[0].annotate(' Earth', (x1[-1], y1[-1]))

numberOfMoonPoints = len(x2) // 10  # only show last 10% of moon trail
axs[0].scatter(x2, y2, s=1, c=range(len(x2)), cmap=blackFade)
axs[0].annotate(' Moon', (x2[-1], y2[-1]))

axs[0].scatter(x3, y3, s=0.1, c=range(len(x3)), cmap=redFade)
axs[0].annotate(' Satellite', (x3[-1], y3[-1]))


# plot the Earth, Moon, and satellite in rotating frame
axs[1].scatter(x1, y1, s=30, c='blue')
axs[1].annotate(' Earth', (x1[-1], y1[-1]))

axs[1].scatter(x2[0], y2[0], s=1, c='black')
axs[1].annotate(' Moon', (x2[0], y2[0]))

axs[1].scatter(rx3, ry3, s=0.1, c=range(len(x3)), cmap=redFade)
axs[1].annotate(' Satellite', (rx3[-1], ry3[-1]))


plot.show()
