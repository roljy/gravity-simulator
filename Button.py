# Button.py
# Tawfeeq Mannan
# Last updated 2021/03/18

# imports
import pygame


# class definition
class Button:
    def __init__(self, x, y, w, h, c, \
        state=True, disabled=False, hold=False, img="img/default.png"):
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
