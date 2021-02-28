import random

color_list = [(255, 0, 0), (255, 51, 51), (255, 102, 102), (255, 153, 153)]
BRICK_WIDTH = 40
BRICK_HEIGHT = 40
bricks = {}


class Brick:
    
    def __init__(self, brick_id, rect=(0, 0, BRICK_WIDTH, BRICK_HEIGHT), hardness=1, width=4):
        self.brick_id=brick_id
        self.rect = (rect[0] + width/2, rect[1] + width/2, rect[2] - width, rect[3] - width)
        self.pos = (rect[0], rect[1])
        self.brick_width = rect[2]
        self.brick_height = rect[3]
        self.hardness = hardness
        self.color = get_color(hardness)
        self.width = width
        self.update_brick()

    def update_brick(self):
        bricks[self.brick_id] = self
    
    def del_brick(self):
        del(bricks[self.brick_id])
    
    def set_pos(self, pos):
        self.pos = pos
        self.rect = (pos[0] + self.width/2, pos[1] + self.width/2, self.rect[2], self.rect[3])
        self.update_brick()
    
    def set_size(self, brick_width, brick_height):
        self.brick_width = brick_width
        self.brick_height = brick_height
        self.rect = (self.rect[0], self.rect[1], brick_width - self.width, brick_height - self.width)
        self.update_brick()
    
    def print_brick(self):
        print("brick_id: {}, rect: {}, hardness: {}, color: {}".format(self.brick_id, self.rect, self.hardness, self.color))


def get_color(hardness, d=5):
    """
    Get the color corresponding to the hardness of the brick.

    param
    hardness(int): the hardness of the brick
    d(int): interval to change the color

    return
    color(tuple): the color, (r, g, b), corresponding to the given hardness
    """

    color_idx = min((hardness - 1)//d, len(color_list) - 1)
    return color_list[color_idx]


def create_random_bricks(max_num, num_level, hardness_level, last_brick_id=-1):
    """
    Create random bricks.

    param
    max_num(int): the maximum number of the bricks that can be created in one row
    num_level(int): param num_level detemines the number of the bricks.
    brick_level(int): param brick_level detemines the brick_num of the bricks.
    last_brick_id(int): the id of last brick

    return
    None
    """

    rand_idx = [i for i in range(max_num)]
    random.shuffle(rand_idx)
    rand_idx = rand_idx[:num_level]
    i = 1
    for idx in rand_idx:

        if random.random()>0.7: continue

        brick_id = last_brick_id + i
        i += 1
        hardness = round(random.uniform(0.7, 1.0)*hardness_level)
        brick = Brick(brick_id=brick_id, hardness=hardness)
        brick.set_pos((idx*BRICK_WIDTH, 2*BRICK_HEIGHT))
        # brick.print_brick()


def process_falling(screen_width, screen_height):
    """
    Every brick will fall down one line, and then new bricks will be created at the top.
    Additionally, check whether the lowest brick hits the bottom.

    param
    screen_width(int): width of the screen
    screen_height(int): height of the screen

    return
    (boolean) True if the lowest brick does not hit the bottom, False otherwise
    """

    last_brick_id = -1
    hit = True
    for brick in bricks.values():

        last_brick_id = max(last_brick_id, brick.brick_id)

        prev_pos = brick.pos
        cur_pos = (prev_pos[0], prev_pos[1] + BRICK_HEIGHT)
        brick.set_pos(cur_pos)

        if hit and cur_pos[1]>=(screen_height - 2*BRICK_HEIGHT): hit = False
    
    max_num = screen_width//BRICK_WIDTH
    num_level = min(max_num, last_brick_id//max_num)
    hardness_level = last_brick_id//max_num + 1
    create_random_bricks(max_num, num_level, hardness_level, last_brick_id)

    return hit