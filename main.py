# main.py
# Tawfeeq Mannan

# imports
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from matplotlib.colors import LinearSegmentedColormap
from setup import helpMsg, getCelestials, allCelestials, allStaticBodies, \
    daysList, trimList


# global vars
celestials = []
fig = plt.figure()
ax = fig.add_subplot(111)


# function definitions
def stripLists(trimAmount, *lists):
    for lst in lists:
        lst[:] = lst[::trimAmount]


# welcome message
print("\nThanks for using my gravity simulator!")
print("I've prepared 5 demo setups, or you can create one on your own!")
print("When the image eventually loads, remember to fullscreen it for \
best results.")
print("The path of each body will be shown by dotted lines, going from \
cyan to magenta as time passes.")
print("Go ahead and enter a number for your selection below:")


plt.rcParams["image.cmap"] = "cool"

# select system to simulate based on user input
print('\n' + helpMsg)
choice = 0
while True:
    try:
        prompt = "Enter the number for the system of your choice: "
        choice = int(input(prompt))
        if not 0 <= choice <= len(allCelestials):
            raise ValueError
        print()
        break
    except ValueError:
        print("Please enter an integer between 0 and 5.\n")


# use user choice to define variables
staticBodies = []
DAYS = 0
TRIM = 0

if choice != 0:
    celestials = allCelestials[choice - 1]
    staticBodies = allStaticBodies[choice - 1]
    DAYS = daysList[choice - 1]
    TRIM = trimList[choice - 1]
else:
    celestials, staticBodies, DAYS = getCelestials()
    TRIM = 60


# wrap up variable declarations/definitions
t = 0
T_STEP = 60
T_TOTAL = DAYS * 24 * 3600


# motion execution
print("Celestial bodies loaded. Running simulation...")
collision = False
while t <= T_TOTAL:
    for i in range(len(celestials)):
        if i in staticBodies:
            continue
        otherMasses = [c for j, c in enumerate(celestials) if \
            j != i and c.mu != 0]
        if not celestials[i].move(otherMasses, T_STEP):
            collision = True
            break
    
    if collision:
        print("Collision detected at", t, "seconds")
        print('(' + str(t // 3600 // 24) + ' days)')
        break

    t += T_STEP

print("Simulation complete. Plotting celestial positions on grid...")
for c in celestials:
    stripLists(TRIM, c.x, c.y, c.vx, c.vy)


# prepare graph axes, titles
timeString = ""
minutes = TRIM * T_STEP // 60
if 60 <= minutes < 120:
    timeString = "hour"
elif minutes >= 120:
    timeString = str(minutes // 60) + " hours"
elif minutes == 1:
    timeString = "minute"
else:
    timeString = str(minutes) + " minutes"

fig.suptitle("Positions of " + str(len(celestials)) + \
    " bodies every " + timeString + " over the course of " + \
        str(t // 3600 // 24) + " days")

ax.axis([-820000, 820000, -500000, 500000])
ax.grid(b=True, which="major")
ax.grid(b=True, which="minor", alpha=0.2)
ax.minorticks_on()
ax.set_axisbelow(True)

ax.set(xlabel="Distance across x-axis (km)", \
    ylabel="Distance across y-axis (km)")


# plot
for c in celestials:
    dotSize = c.r / 500 if c.r != 0 else 0.5
    ax.scatter(c.x, c.y, s=dotSize, c=range(len(c.x)), cmap="cool")

    ax.annotate(celestials.index(c) + 1, (c.x[-1], c.y[-1]), \
        xytext=(c.x[-1] + 20000, c.y[-1] + 20000), \
        arrowprops={"arrowstyle": "->"}, color="green", weight="bold")

fig.subplots_adjust(left=0.125, right=0.875, top=0.95, bottom=0.05)
print("Plotting complete. Loading graph...")

plt.show()


# exit message
print("\nTo run another simulation, you can restart this program.")
input("Press Enter to quit the program: ")
print("Thanks for using the gravity simulator!")
