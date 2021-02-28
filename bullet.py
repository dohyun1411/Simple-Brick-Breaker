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


def collision_checker(rect, circle):
    """
    Check whether the rectangles collides with the circle.

    param
    circle(tuple): circle information, (center, radius)
    rect(tuple): rectangle information, (left, top, width, height)

    return
    (int) 0 if there is no collision,
          1 if the circle collides with the top/bottom of the rectangle
          2 if the circle collides with the left/right side of the rectangle          
    """

    r_left, r_top, r_width, r_height = rect
    r_right = r_left + r_width
    r_bottom = r_top + r_height
    
    center_x, center_y = circle[0]
    radius = circle[1]
    c_left = center_x - radius
    c_right = center_x + radius
    c_top = center_y - radius
    c_bottom = center_y + radius

    dx = min(abs(left - center_x), abs(right - center_x))
    dy = min(abs(top - center_y), abs(bottom - center_y))

    if dx<=radius:
        print(rect, circle)
        return 2
    if dy<=radius:
        return 1
    return 0

