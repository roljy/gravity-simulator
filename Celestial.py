# Celestial.py
# Tawfeeq Mannan
# Last updated 2021/03/20

# imports
from math import sqrt, sin, cos, atan, pi


# class definition
class Celestial:
    def __init__(self, x, y, vx=0, vy=0, Gm=0, r=0, c=(255, 0, 0)):
        self.x = x
        self.y = y
        self.vx = vx
        self.vy = vy
        self.mu = Gm
        self.r = r
        self.colour = c
    

    def get_copy(self):
        copy = Celestial(self.x, self.y, self.vx, self.vy, \
            self.mu, self.r, self.colour)
        return copy


    def get_scalar_distance_to(self, x, y):
        return sqrt((self.x - x) ** 2 + (self.y - y) ** 2)


    def move(self, celestials, timeStep, forwardsTime=True, gravity=True):
        ax, ay = 0, 0
        crashedWith = 0
        for c in celestials:
            # check for collision
            if c.get_scalar_distance_to(self.x, self.y) < c.r + self.r:
                crashedWith = c
        
            # add gravitational field (negative) of all the other bodies
            if gravity:
                ax -= (c.mu * (self.x - c.x)) / \
                    c.get_scalar_distance_to(self.x, self.y) ** 3
                ay -= (c.mu * (self.y - c.y)) / \
                    c.get_scalar_distance_to(self.x, self.y) ** 3
            
        # integrate acceleration to get new velocities and positions
        if forwardsTime:
            self.vx = self.vx + ax * timeStep
            self.vy = self.vy + ay * timeStep
            self.x = self.x + self.vx * timeStep
            self.y = self.y + self.vy * timeStep
        else:
            self.vx = self.vx - ax * timeStep
            self.vy = self.vy - ay * timeStep
            self.x = self.x - self.vx * timeStep
            self.y = self.y - self.vy * timeStep
        
        return crashedWith

    
    def maneuver(self, tangent=True, dv=0, dvx=0, dvy=0):
        # assume forwards time. no maneuvers allowed in backwards time
        if tangent:
            try:
                angle = atan(self.vy / self.vx)
            except ZeroDivisionError:
                angle = pi / 2
            if self.vx <= 0 and self.vy <= 0:
                angle += pi  # Q1 --> Q3, pi/2 --> 3pi/2
            elif self.vx <= 0 and self.vy >= 0:
                angle += pi  # Q4 --> Q2
            self.vx = self.vx + dv * cos(angle)
            self.vy = self.vy + dv * sin(angle)
        
        else:
            self.vx += dvx
            self.vy += dvy


# function definitions
def inelastic_collision(a, b):
    totalMass = a.mu + b.mu

    # new velocity components based on conservation of momentum
    px = a.mu * a.vx + b.mu * b.vx
    vx = px / totalMass
    py = a.mu * a.vy + b.mu * b.vy
    vy = py / totalMass
    
    # new position at centre of mass
    x = (a.mu * a.x + b.mu * b.x) / totalMass
    y = (a.mu * a.y + b.mu * b.y) / totalMass

    # new radius to reflect sum of area
    r = sqrt(a.r ** 2 + b.r ** 2)

    # new colour based on larger body
    c = b.colour if b.r > a.r else a.colour

    return Celestial(x, y, vx, vy, totalMass, r, c)


def elastic_collision(a, b):
    totalMass = a.mu + b.mu
    massDiff = b.mu - a.mu

    # calculate relevant angles
    try:
        theta1 = atan(a.vy / a.vx)
    except ZeroDivisionError:
        theta1 = pi / 2

    if a.vx <= 0 and a.vy <= 0:
        theta1 += pi  # Q1 --> Q3, pi/2 --> 3pi/2
    elif a.vx <= 0 and a.vy >= 0:
        theta1 += pi  # Q4 --> Q2

    try:
        theta2 = atan(b.vy / b.vx)
    except ZeroDivisionError:
        theta2 = pi / 2

    if b.vx <= 0 and b.vy <= 0:
        theta2 += pi  # Q1 --> Q3, pi/2 --> 3pi/2
    elif b.vx <= 0 and b.vy >= 0:
        theta2 += pi  # Q4 --> Q2

    try:
        phi = atan( (b.y - a.y) / (b.x - a.x) )
    except ZeroDivisionError:
        phi = pi / 2

    if (b.x - a.x) <= 0 and (b.y - a.y) <= 0:
        phi += pi  # Q1 --> Q3, pi/2 --> 3pi/2
    elif (b.x - a.x) <= 0 and (b.y - a.y) >= 0:
        phi += pi  # Q4 --> Q2
    
    # calculate magnitudes of velocities. needed for equation
    v1 = sqrt(a.vx ** 2 + a.vy ** 2)
    v2 = sqrt(b.vx ** 2 + b.vy ** 2)

    # calculate new velocity components. equation from wikipedia
    vax = (v1 * cos(theta1 - phi) * -massDiff + \
        2 * b.mu * v2 * cos(theta2 - phi)) / totalMass * cos(phi) + \
            v1 * sin(theta1 - phi) * cos(phi + pi / 2)

    vay = (v1 * cos(theta1 - phi) * -massDiff + \
        2 * b.mu * v2 * cos(theta2 - phi)) / totalMass * sin(phi) + \
            v1 * sin(theta1 - phi) * sin(phi + pi / 2)

    vbx = (v2 * cos(theta2 - phi) * massDiff + \
        2 * a.mu * v1 * cos(theta1 - phi)) / totalMass * cos(phi) + \
            v2 * sin(theta2 - phi) * cos(phi + pi / 2)

    vby = (v2 * cos(theta2 - phi) * massDiff + \
        2 * a.mu * v1 * cos(theta1 - phi)) / totalMass * sin(phi) + \
            v2 * sin(theta2 - phi) * sin(phi + pi / 2)
    
    return vax, vay, vbx, vby
