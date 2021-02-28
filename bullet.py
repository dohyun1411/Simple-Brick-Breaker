import math
import random

class Bullet:

    def __init__(self, bullet_id, pos, theta, speed=0.1, radius=5, color=(102, 178, 255), power=1):
        self.bullet_id = bullet_id
        self.pos = pos
        self.theta = theta
        self.speed = speed
        self.radius = radius
        self.color = color
        self.power = power

        self.dx = speed*math.cos(theta*math.pi/180)
        self.dy = speed*math.sin(theta*math.pi/180)