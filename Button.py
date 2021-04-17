# Button.py
# Tawfeeq Mannan
# Last updated 2021/04/17

# imports
import pygame
from abspath import absolute_path
from colour import COLOURS


# class definition
class Button:
    def __init__(self, x, y, w, h, c, \
        state=True, disabled=False, hold=False, \
            img=absolute_path("img/default.png")):
        self.rect = pygame.Rect(x, y, w, h)

        self.colour1 = c[0]  # state 1
        self.colour2 = c[1]  # state 2
        self.colour3 = c[2]  # disabled
        self.isPressed = state
        self.isDisabled = disabled
        self.update_colour()
        
        self.pushToTalk = hold

        self.img = pygame.image.load(img)
    

    def update_colour(self):
        self.colour = self.colour2
        if self.isDisabled:
            self.colour = self.colour3
        elif self.isPressed:
            self.colour = self.colour1


    def handle_event(self, ev):
        # changes button state based on mousepress
        if not self.isDisabled:
            if ev.type == pygame.MOUSEBUTTONDOWN:
                if self.rect.collidepoint(ev.pos):
                    if self.pushToTalk:
                        self.isPressed = True
                    else:
                        self.isPressed = not self.isPressed
            elif ev.type == pygame.MOUSEBUTTONUP:
                if self.pushToTalk:
                    self.isPressed = False
    

    def disable(self):
        self.isPressed = False
        self.isDisabled = True
    

    def enable(self):
        self.isPressed = False
        self.isDisabled = False


    def draw(self, surface):
        self.update_colour()
        pygame.draw.rect(surface, self.colour, self.rect)
        coords = (self.rect.x + (self.rect.width - self.img.get_width()) / 2, \
            self.rect.y + (self.rect.height - self.img.get_height()) / 2)
        surface.blit(self.img, coords)


# buttons
buttons = {
    "gravity" : Button(10, 10, 40, 40, \
        (COLOURS["GREEN"], COLOURS["RED"], COLOURS["GREY"]), \
            state=True, disabled=False, hold=False, \
                img=absolute_path("img/gravity.png")),
    "elastic" : Button(10, 10, 40, 40, \
        (COLOURS["GREEN"], COLOURS["RED"], COLOURS["GREY"]), \
            state=False, disabled=False, hold=False, \
                img=absolute_path("img/elastic.png")),
    "reverse" : Button(10, 10, 40, 40, \
        (COLOURS["GREEN"], COLOURS["RED"], COLOURS["GREY"]), \
            state=False, disabled=False, hold=False, \
                img=absolute_path("img/reverse.png")),
    "playpause" : Button(10, 10, 40, 40, \
        (COLOURS["GREEN"], COLOURS["RED"], COLOURS["GREY"]), \
            state=False, disabled=False, hold=False, \
                img=absolute_path("img/playpause.png")),
    "skip" : Button(10, 10, 40, 40, \
        (COLOURS["GREEN"], COLOURS["RED"], COLOURS["GREY"]), \
            state=False, disabled=False, hold=True, \
                img=absolute_path("img/skip.png")),
}


# function definitions
def reposition_buttons(w, h):
    buttons["gravity"].rect.update(10, 10, 40, 40)
    buttons["elastic"].rect.update(60, 10, 40, 40)
    buttons["reverse"].rect.update(w - 150, 10, 40, 40)
    buttons["playpause"].rect.update(w - 100, 10, 40, 40)
    buttons["skip"].rect.update(w - 50, 10, 40, 40)
