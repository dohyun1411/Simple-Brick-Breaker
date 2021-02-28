import random

BRICK_WIDTH = 40
BRICK_HEIGHT = 40
WIDTH = 4
colors = [(255, 153, 153), (255, 102, 102), (255, 51, 51), (255, 0, 0)]


class Brick:

    def __init__(self, brick_id, pos=(0, 0), brick_width=BRICK_WIDTH, brick_height=BRICK_HEIGHT, width=WIDTH, hardness=1, colors=colors):
        self.brick_id = brick_id
        self.pos = pos
        self.brick_width = brick_width
        self.brick_height = brick_height
        self.hardness = hardness
        self.width = width
        self.colors = colors

        self.rect = (pos[0] + width/2, pos[1] + width/2, brick_width - width, brick_height - width)     
        self.color = self.get_color()

    def set_pos(self, pos):
        self.pos = pos
        self.rect = (pos[0] + self.width/2, pos[1] + self.width/2, self.rect[2], self.rect[3])
    
    def set_size(self, brick_width, brick_height):
        self.brick_width = brick_width
        self.brick_height = brick_height
        self.rect = (self.rect[0], self.rect[1], brick_width - self.width, brick_height - self.width)
    
    def print_brick(self):
        print("brick_id: {}, pos: {}, brick_width: {}, brick_height: {}, hardness: {}, color: {}".format(self.brick_id, self.pos, self.brick_width, self.brick_height, self.hardness, self.color))


    def get_color(self, d=5):
        """
        Get the color corresponding to the hardness of the brick.

        param
        d(int): interval to change the color

        return
        color(tuple): the color, (r, g, b), corresponding to the given hardness
        """

        color_idx = min((self.hardness - 1)//d, len(self.colors) - 1)
        return self.colors[color_idx]


def create_random_bricks(bricks, max_num, num_level, hardness_level, last_brick_id=-1):
    """
    Create random bricks.

    param
    bricks(dictionary): the store of the bricks
    max_num(int): the maximum number of the bricks that can be created in one row
    num_level(int): param num_level detemines the number of the bricks.
    brick_level(int): param brick_level detemines the brick_num of the bricks.
    last_brick_id(int): the id of last brick

    return
    bricks(dictionary): the store of the bricks (updated)
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
        bricks[brick.brick_id] = brick
        # brick.print_brick()
    
    return bricks


def process_falling(bricks, screen_width, screen_height):
    """
    Every brick will fall down one line, and then new bricks will be created at the top.
    Additionally, check whether the lowest brick hits the bottom.

    param
    bricks(dictionary): the store of the bricks
    screen_width(int): width of the screen
    screen_height(int): height of the screen

    return
    (bool) True if the lowest brick does not hit the bottom, False otherwise
    bricks(dictionary): the store of the bricks (updated)
    """

    last_brick_id = -1
    hit = True
    for brick in bricks.values():

        last_brick_id = max(last_brick_id, brick.brick_id)

        prev_pos = brick.pos
        cur_pos = (prev_pos[0], prev_pos[1] + BRICK_HEIGHT)
        brick.set_pos(cur_pos)
        bricks[brick.brick_id] = brick

        if hit and cur_pos[1]>=(screen_height - 2*BRICK_HEIGHT): hit = False
    
    max_num = screen_width//BRICK_WIDTH
    num_level = random.randint(1, max_num) # TO DO: find proper num_level
    hardness_level = last_brick_id//max_num + 1
    bricks = create_random_bricks(bricks, max_num, num_level, hardness_level, last_brick_id)

    return hit, bricks