# Celestial.py
# Tawfeeq Mannan

# imports
from math import sqrt, sin, cos, atan, pi


# class definitions
class Celestial:
    def __init__(self, x, y, vx=0, vy=0, Gm=0, r=0):
        self.x = [x]
        self.y = [y]
        self.vx = [vx]
        self.vy = [vy]
        self.mu = Gm
        self.r = r


    def getScalarDistanceTo(self, x, y, forwardsTime=True):
        index = -1 if forwardsTime else 0
        return sqrt((self.x[index] - x) ** 2 + (self.y[index] - y) ** 2)


    def move(self, celestials, timeStep, forwardsTime=True):
        index = -1 if forwardsTime else 0
        ax, ay = 0, 0
        for c in celestials:
            ax -= (c.mu * (self.x[index] - c.x[index])) / \
                c.getScalarDistanceTo(self.x[index], self.y[index], \
                    forwardsTime) ** 3
            ay -= (c.mu * (self.y[index] - c.y[index])) / \
                c.getScalarDistanceTo(self.x[index], self.y[index], \
                    forwardsTime) ** 3
            # if abs(ax) > 0.1 or abs(ay) > 0.1:
            if c.getScalarDistanceTo(self.x[index], self.y[index], \
                forwardsTime) < c.r + self.r:
                return False
        
        if forwardsTime:
            self.vx.append(self.vx[index] + ax * timeStep)
            self.vy.append(self.vy[index] + ay * timeStep)
            self.x.append(self.x[index] + self.vx[index] * timeStep)
            self.y.append(self.y[index] + self.vy[index] * timeStep)
        else:
            self.vx.insert(index, self.vx[index] - ax * timeStep)
            self.vy.insert(index, self.vy[index] - ay * timeStep)
            self.x.insert(index, self.x[index] - self.vx[index] * timeStep)
            self.y.insert(index, self.y[index] - self.vy[index] * timeStep)
        
        return True

    
    def maneuver(self, tangent=True, dv=0, dvx=0, dvy=0):
        # assume forwards time. no maneuvers allowed in backwards time
        if tangent:
            angle = atan(self.vy[-1] / self.vx[-1])
            if self.vx[-1] <= 0 and self.vy[-1] <= 0:
                angle += pi  # Q1 --> Q3
            elif self.vx[-1] <= 0 and self.vy[-1] >= 0:
                angle += pi  # Q4 --> Q2
            self.vx.append(self.vx[-1] + dv * cos(angle))
            self.vy.append(self.vy[-1] + dv * sin(angle))
        
        else:
            self.vx.append(self.vx[-1] + dvx)
            self.vy.append(self.vy[-1] + dvy)
