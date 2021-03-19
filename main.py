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

DAYS = 80  # total time to simulate for (days)
BDAYS = 2  # number of days to integrate in negative time
T_STEP = 60  # integration step size (seconds)
T_TOTAL = DAYS * 24 * 3600
TRIM = 60 # trim every how many data points


# variables
def resetToInitialPositions():
    global t, theta, vx, vy
    t = 0
    theta = 0

    vx = 0
    vy = 8.81

resetToInitialPositions()

x2 = [R * cos(theta)]
y2 = [R * sin(theta)]

x3 = [10000]
y3 = [0]
rx3 = [x3[0]]
ry3 = [y3[0]]


# preparation of maneuvers
MANEUVERS = [
]
totalDeltaV = round(sum(abs(m[1]) for m in MANEUVERS) * 1000, 1)


# initialize matplotlib subplots (1x2, labels, axes, gridlines)
fig, axs = plot.subplots(nrows=1, ncols=2, sharex=False, sharey=False)
fig.suptitle('Position of a satellite every hour as it is maneuvered through ' + \
    'the Earth-Moon system in the lunar plane over a span of ' + str(DAYS) + \
        ' days \nInitial orbit radius: ' + \
            str(round(sqrt(x3[0] ** 2 + y3[0] ** 2))) + ' km\n' + \
                'Total Δv: ' + str(totalDeltaV) + ' m/s')
axs[0].set_title('Motion of satellite in inertial reference frame')
axs[1].set_title('Motion of satellite in rotating reference frame')
for ax in axs:
    ax.set(xlabel='Distance along x-axis (km)', \
        ylabel='Distance along y-axis (km)')
    # ax.label_outer()
    ax.axis([-500000, 500000, -562500, 562500])
    ax.grid(b=True, which='major')
    ax.grid(b=True, which='minor', alpha=0.2)
    ax.minorticks_on()
    ax.set_axisbelow(True)


# simulation functions
def getDistanceToSatellite(body=1, forwardsTime=True):
    if body == 1 and forwardsTime:
        return sqrt((x3[-1] - x1[-1]) ** 2 + (y3[-1] - y1[-1]) ** 2)
    elif body == 1 and not forwardsTime:
        return sqrt((x3[0] - x1[0]) ** 2 + (y3[0] - y1[0]) ** 2)
    elif body == 2 and forwardsTime:
        return sqrt((x3[-1] - x2[-1]) ** 2 + (y3[-1] - y2[-1]) ** 2)
    elif body == 2 and not forwardsTime:
        return sqrt((x3[0] - x2[0]) ** 2 + (y3[0] - y2[0]) ** 2)


def moveMoonInInertialFrame(forwardsTime=True):
    global R, OMEGA, T_STEP, theta, x2, y2
    if forwardsTime:
        theta += OMEGA * T_STEP
        x2.append(R * cos(theta))
        y2.append(R * sin(theta))

        # return true if Moon has completed sidereal revolution
        return y2[-1] > 0 and y2[-2] < 0

    else:
        theta -= OMEGA * T_STEP
        x2.insert(0, R * cos(theta))
        y2.insert(0, R * sin(theta))
        return y2[0] < 0 and y2[1] > 0


def moveSatelliteInInertialFrame(forwardsTime=True):
    global M1, M2, x1, y1, T_STEP, x2, y2, x3, y3, vx, vy
    if forwardsTime:
        ax = - (M1 * (x3[-1] - x1[-1])) \
            / getDistanceToSatellite(1, True) ** 3 \
                - (M2 * (x3[-1] - x2[-1])) \
                    / getDistanceToSatellite(2, True) ** 3
        
        ay = - (M1 * (y3[-1] - y1[-1])) \
            / getDistanceToSatellite(1, True) ** 3 \
                - (M2 * (y3[-1] - y2[-1])) \
                    / getDistanceToSatellite(2, True) ** 3
        
        vx += ax * T_STEP
        vy += ay * T_STEP
        x3.append(x3[-1] + vx * T_STEP)
        y3.append(y3[-1] + vy * T_STEP)

        # return true if satellite has completed sidereal revolution
        return y3[-1] > 0 and y3[-2] < 0
    
    else:
        ax = - (M1 * (x3[0] - x1[0])) \
            / getDistanceToSatellite(1, False) ** 3 \
                - (M2 * (x3[0] - x2[0])) \
                    / getDistanceToSatellite(2, False) ** 3
        ay = - (M1 * (y3[0] - y1[0])) \
            / getDistanceToSatellite(1, False) ** 3 \
                - (M2 * (y3[0] - y2[0])) \
                    / getDistanceToSatellite(2, False) ** 3
        vx -= ax * T_STEP
        vy -= ay * T_STEP
        x3.insert(0, x3[0] - vx * T_STEP)
        y3.insert(0, y3[0] - vy * T_STEP)
        return y3[0] < 0 and y3[1] > 0


def recordSatelliteInRotatingFrame(forwardsTime=True):
    global x1, y1, theta, x3, y3, rx3, ry3
    if forwardsTime:
        dist = getDistanceToSatellite(1, True)
        angle = atan((y3[-1] - y1[-1]) / (x3[-1] - x1[-1]))
        if x3[-1] - x1[-1] < 0 and y3[-1] - y1[-1] > 0:
            angle += pi  # convert from Q4 to Q2
        elif x3[-1] - x1[-1] < 0 and y3[-1] - y1[-1] < 0:
            angle += pi  # convert from Q1 to Q3
        
        dTheta = angle - theta
        rx3.append(dist * cos(dTheta))
        ry3.append(dist * sin(dTheta))
    
    else:
        dist = getDistanceToSatellite(1, False)
        angle = atan((y3[0] - y1[0]) / (x3[0] - x1[0]))
        if x3[0] - x1[0] < 0 and y3[0] - y1[0] > 0:
            angle += pi  # convert from Q4 to Q2
        elif x3[0] - x1[0] < 0 and y3[0] - y1[0] < 0:
            angle += pi  # convert from Q1 to Q3
        dTheta = angle - theta
        rx3.insert(0, dist * cos(dTheta))
        ry3.insert(0, dist * sin(dTheta))


# function to execute satellite maneuver
def maneuver(deltaV):
    global vx, vy
    angle = atan(vy / vx)
    if vx < 0 and vy > 0:
        angle += pi  # Q4 --> Q2
    elif vx < 0 and vy < 0:
        angle += pi  # Q1 --> Q3
    vx += deltaV * cos(angle)
    vy += deltaV * sin(angle)


# function to reduce the number of data points to clean up the scatter plot
def trimLists(trimAmount, *lists):
    for lst in lists:
        lst[:] = lst[::trimAmount]


# execution of satellite motion
closestApproach, approachTime = 999999999999, 0
highestPotential, potentialTime = -999999999999, 0
while t <= T_TOTAL:
    for m in MANEUVERS:
        if t == m[0]:
            maneuver(m[1])

    moveMoonInInertialFrame()
    moveSatelliteInInertialFrame()
    recordSatelliteInRotatingFrame()

    if getDistanceToSatellite(1, True) < 6371.0:
        print('Collided with the Earth at ' + str(t) + ' seconds.')
        break

    potential = (vx ** 2 + vy ** 2) / 2 - M1 / getDistanceToSatellite(1, True)
    if potential > highestPotential:
        highestPotential = potential
        potentialTime = t

    if getDistanceToSatellite(2, True) < closestApproach:
        closestApproach = getDistanceToSatellite(2, True)
        approachTime = t
    if closestApproach < 1737.4:
        print('Collided with the Moon at ' + str(t) + ' seconds.')
        break

    t += T_STEP

print('Closest approach in forwards time:', closestApproach, 'km at', \
    approachTime, 'seconds.')
print('Highest potential in forwards time:', highestPotential, 'km2/s2 at', \
    potentialTime, 'seconds.')


# execution of reverse satellite motion
resetToInitialPositions()
closestApproach, approachTime = 999999999999, 0
highestPotential, potentialTime = -999999999999, 0
while t >= - BDAYS * 24 * 3600:
    moveMoonInInertialFrame(forwardsTime=False)
    moveSatelliteInInertialFrame(forwardsTime=False)
    recordSatelliteInRotatingFrame(forwardsTime=False)
    if getDistanceToSatellite(1, False) < 6371.0:
        print('Collided with the Earth at ' + str(t) + ' seconds.')
        break
    potential = (vx ** 2 + vy ** 2) / 2 - M1 / getDistanceToSatellite(1, False)
    if potential > highestPotential:
        highestPotential = potential
        potentialTime = t
    if getDistanceToSatellite(2, False) < closestApproach:
        closestApproach = getDistanceToSatellite(2, False)
        approachTime = t
    if closestApproach < 1737.4:
        print('Collided with the Moon at ' + str(t) + ' seconds.')
        break
    t -= T_STEP
print('Closest approach in backwards time:', closestApproach, 'km at', \
    approachTime, 'seconds.')
print('Highest potential in backwards time:', highestPotential, 'km2/s2 at', \
    potentialTime, 'seconds.')


# slimming down the data
trimLists(TRIM, x2, y2, x3, y3, rx3, ry3)


# defining colormaps to fade the satellite path history
redFadeDict = {
    'red': [(0, 1, 1), (1, 1, 1)],
    'green': [(0, 0.7, 0.7), (0.5, 0.4, 0.4), (0.9, 0.2, 0.2), (1, 0, 0)],
    'blue': [(0, 0.7, 0.7), (0.5, 0.4, 0.4), (0.9, 0.2, 0.2), (1, 0, 0)]
}
blackFadeDict = {
    'red': [(0, 0.9, 0.9), \
        ((1 - 27 / (DAYS + BDAYS) if DAYS > (27 - BDAYS) else 0.7), 0.7, 0.7), \
            (1, 0, 0)],
    'green': [(0, 0.9, 0.9), \
        ((1 - 27 / (DAYS + BDAYS) if DAYS > (27 - BDAYS) else 0.7), 0.7, 0.7), \
            (1, 0, 0)],
    'blue': [(0, 0.9, 0.9), \
        ((1 - 27 / (DAYS + BDAYS) if DAYS > (27 - BDAYS) else 0.7), 0.7, 0.7), \
            (1, 0, 0)]
}
redFade = LinearSegmentedColormap('', redFadeDict)
blackFade = LinearSegmentedColormap('', blackFadeDict)


# plot the Earth, Moon, and satellite in inertial frame
resetToInitialPositions()
x2.insert(0, R * cos(theta))
y2.insert(0, R * sin(theta))

axs[0].scatter(x1, y1, s=30, c='blue')
axs[0].annotate(' Earth', (x1[-1], y1[-1]))

numberOfMoonPoints = len(x2) // 10  # only show last 10% of moon trail
axs[0].scatter(x2, y2, s=1, c=range(len(x2)), cmap=blackFade)
axs[0].annotate(' Moon', (x2[-1], y2[-1]))

axs[0].scatter(x3, y3, s=0.1, c=range(len(x3)), cmap='cool')
axs[0].annotate(' Satellite', (x3[-1], y3[-1]))

axs[0].annotate('/~>', (x3[BDAYS * 24], y3[BDAYS * 24]))


# plot the Earth, Moon, and satellite in rotating frame
axs[1].scatter(x1, y1, s=30, c='blue')
axs[1].annotate(' Earth', (x1[-1], y1[-1]))

axs[1].scatter(x2[0], y2[0], s=1, c='black')
axs[1].annotate(' Moon', (x2[0], y2[0]))

axs[1].scatter(rx3, ry3, s=0.1, c=range(len(x3)), cmap='cool')
axs[1].annotate(' Satellite', (rx3[-1], ry3[-1]))

axs[1].annotate('/~>', (rx3[BDAYS * 24], ry3[BDAYS * 24]))


# annotate maneuver nodes
for m in MANEUVERS:
    tag = 'Δv' + str(MANEUVERS.index(m) + 1)
    index = int(m[0] + BDAYS * 24 * 3600) // 3600
    axs[0].annotate('/~> ' + tag, (x3[index], y3[index]), color='magenta')
    axs[1].annotate('/~> ' + tag, (rx3[index], ry3[index]), color='magenta')


plot.show()
