# gravity.py
# Tawfeeq Mannan
# Last updated 2021/03/20

# imports
import pygame
import sys
from abspath import absolute_path
from Button import Button
from Celestial import inelastic_collision, elastic_collision
from setup import helpMsg, getCelestials, allCelestials, allStaticBodies


# consts
WIDTH = 1280
HEIGHT = 720
T_STEP = 360
COLOURS = {
    "BLACK" : (0, 0, 0),
    "WHITE" : (255, 255, 255),
    "GREY" : (127, 127, 127),
    "RED" : (255, 0, 0),
    "ORANGE" : (255, 160, 0),
    "YELLOW" : (255, 255, 0),
    "GREEN" : (0, 255, 0),
    "CYAN" : (0, 255, 255),
    "PINK" : (255, 0, 160),
}


# global vars
celestials = []
t = 0
FPS = 120
lastCollisionTime = 0
runAgain = True
isRunning = True


# buttons
buttons = {
    "gravity" : Button(10, 10, 40, 40, \
        (COLOURS["GREEN"], COLOURS["RED"], COLOURS["GREY"]), \
            state=True, disabled=False, hold=False, \
                img=absolute_path("img/gravity.png")),
    "elastic" : Button(60, 10, 40, 40, \
        (COLOURS["GREEN"], COLOURS["RED"], COLOURS["GREY"]), \
            state=False, disabled=False, hold=False, \
                img=absolute_path("img/elastic.png")),
    "reverse" : Button(WIDTH - 150, 10, 40, 40, \
        (COLOURS["GREEN"], COLOURS["RED"], COLOURS["GREY"]), \
            state=False, disabled=False, hold=False, \
                img=absolute_path("img/reverse.png")),
    "playpause" : Button(WIDTH - 100, 10, 40, 40, \
        (COLOURS["GREEN"], COLOURS["RED"], COLOURS["GREY"]), \
            state=False, disabled=False, hold=False, \
                img=absolute_path("img/playpause.png")),
    "skip" : Button(WIDTH - 50, 10, 40, 40, \
        (COLOURS["GREEN"], COLOURS["RED"], COLOURS["GREY"]), \
            state=False, disabled=False, hold=True, \
                img=absolute_path("img/skip.png")),
}


# function definitions
def reset():
    global celestials, t, FPS, lastCollisionTime, runAgain, isRunning, buttons
    celestials = []
    t = 0
    FPS = 120
    lastCollisionTime = 0
    runAgain = True
    isRunning = True
    buttons["gravity"].isPressed = True
    buttons["elastic"].isPressed = False
    buttons["reverse"].isPressed = False
    buttons["playpause"].isPressed = False
    buttons["skip"].isPressed = False


def move_bodies(forwardsTime, gravity, previousCollisions):
    global celestials, t, lastCollisionTime, T_STEP
    collisions = set()

    # move all bodies and record all collision pairs
    for i in range(len(celestials)):
        if i in staticBodies:
            continue

        otherMasses = [c for j, c in enumerate(celestials) if \
            j != i and c.mu != 0]
        contact = celestials[i].move(otherMasses, T_STEP, \
            forwardsTime, gravity)
        
        if contact:
            j = celestials.index(contact)
            collisions.add( (min(i, j), max(i, j)) )

    # do not re-simulate a collision that just happened last frame
    if not collisions == previousCollisions:
        for collision in collisions:
            i, j = collision
            elasticOverride = False

            # elastic collision
            if buttons["elastic"].isPressed:
                v1 = celestials[i].vx ** 2 + celestials[i].vy ** 2
                v2 = celestials[j].vx ** 2 + celestials[j].vy ** 2
                if buttons["gravity"].isPressed and (v1 < 1 or v2 < 1 or \
                    t - lastCollisionTime <= T_STEP * 10):
                    # do inelastic collision if scuffed
                    print("Elastic collision overridden to inelastic.")
                    elasticOverride = True
                else:
                    celestials[i].vx, celestials[i].vy, \
                        celestials[j].vx, celestials[j].vy = \
                            elastic_collision(celestials[i], celestials[j])
                    print("Collision detected at", t, "seconds")
                    print('(' + str(t // 3600 // 24) + ' days)')

            # inelastic collision
            if not buttons["elastic"].isPressed or elasticOverride:
                merged = inelastic_collision(celestials[i], celestials[j])
                celestials.pop(j)
                celestials.pop(i)
                celestials.append(merged)
                print("Collision detected at", t, "seconds")
                print('(' + str(t // 3600 // 24) + ' days)')

    # update time
    lastCollisionTime = t if collisions else lastCollisionTime
    timeChange = T_STEP * (-1 if buttons["reverse"].isPressed else 1)
    t += timeChange
    return collisions


def draw_bodies(surface):
    global celestials
    for i in range(len(celestials)):
        x = WIDTH / 2 + celestials[i].x / 1500
        y = HEIGHT / 2 - celestials[i].y / 1500
        dotSize = celestials[i].r / 1500 if celestials[i].r > 1500 else 1
        colour = list(COLOURS.values())[i % (len(COLOURS) - 3) + 3]
        pygame.draw.circle(surface, colour, (x, y), dotSize)


# welcome message
print("\nThanks for using my gravity simulator!")
print("I've prepared 6 demo setups, or you can create one on your own!")
print("The simulation opens in a new window. You may need to click on it.")
print("Go ahead and enter a number for your selection below:")


while runAgain:
    reset()

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
            print("Please enter an integer between 0 and 6.\n")


    # use user choice to define variables
    staticBodies = []

    if choice != 0:
        celestials = [c.get_copy() for c in allCelestials[choice - 1]]
        staticBodies = allStaticBodies[choice - 1].copy()
    else:
        celestials, staticBodies = getCelestials()


    # initialize pygame
    pygame.init()
    SCREEN = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Gravity Simulator")
    pygame.display.set_icon(pygame.image.load(absolute_path("img/planets.ico")))
    clock = pygame.time.Clock()


    # game loop
    print("Celestial bodies loaded. Running simulation...")
    lastCollisions, collTime = set(), 0  # for debouncing
    while isRunning:
        # screen refresh
        clock.tick(FPS)
        SCREEN.fill(COLOURS["BLACK"])

        # event handling (button presses, quit)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                isRunning = False

            for button in buttons.values():
                button.handle_event(event)
        
        # motion execution
        collisions = set()

        if buttons["playpause"].isPressed and buttons["skip"].isPressed:
            FPS = 360  # fast forward
            collisions = move_bodies(not buttons["reverse"].isPressed, \
                buttons["gravity"].isPressed, lastCollisions)

        elif buttons["playpause"].isPressed or buttons["skip"].isPressed:
            FPS = 120  # normal speed
            collisions = move_bodies(not buttons["reverse"].isPressed, \
                buttons["gravity"].isPressed, lastCollisions)
        
        lastCollisions = collisions

        # draw all celestials and update screen
        draw_bodies(SCREEN)
        for button in buttons.values():
            button.draw(SCREEN)

        pygame.display.update()


    # close pygame window
    pygame.display.quit()
    pygame.quit()
    

    # ask for repetition
    again = input("\nDo you want to run the simulation again? (y/n) ")
    if not again.lower().startswith('y'):
        runAgain = False


# cleanup and exit
sys.exit()
