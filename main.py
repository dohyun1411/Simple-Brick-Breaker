import os
import random
import pygame
import brick as br
import bullet as bu


if __name__=="__main__":

    pygame.init()

    SCREEN_WIDTH = 480
    SCREEN_HEIGHT = 640
    BRICK_WIDTH = 40
    BRICK_HEIGHT = 40
    WALL_HEIGHT = 5
    WHITE = (255, 255, 255)
    BLACK = (0, 0, 0)

    current_path = os.path.dirname(__file__)
    image_path = os.path.join(current_path, "images")

    arrow = pygame.image.load(os.path.join(image_path, "arrow.png"))

    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    screen.fill(WHITE)

    hardness_font = pygame.font.Font(None, 25)
    score_font = pygame.font.Font(None, 30)
    
    pygame.display.set_caption("swipe_brick_breaker")

    
    running = True
    bricks = {}
    bullets = {}
    start_ticks = pygame.time.get_ticks()
    prev_step = 0
    prev_shooting_step = 0
    last_bullet_id = 0
    theta = 90
    dtheta = 0
    angular_speed = 0.05
    bullet_speed = 0.1
    radius = 5
    GUN_RECT = (220, 600, 40, 40)
    GUN_WIDTH = 3
    GUN_POS = (240, 620)
    arrow_x, arrow_y = 237.5, 605

    while running:

        screen.fill(WHITE)
        pygame.draw.circle(screen, (102, 178, 255), GUN_POS, 20, GUN_WIDTH)
        # pygame.draw.rect(screen, (102, 178, 255), GUN_RECT, width=GUN_WIDTH)
        pygame.draw.rect(screen, BLACK, (0, 2*BRICK_HEIGHT - WALL_HEIGHT, SCREEN_WIDTH, WALL_HEIGHT))

        for event in pygame.event.get():
            if event.type==pygame.QUIT: running = False

            if event.type==pygame.KEYDOWN:
                if event.key==pygame.K_LEFT:
                    dtheta += angular_speed
                if event.key==pygame.K_RIGHT:
                    dtheta -= angular_speed
            
            if event.type==pygame.KEYUP:
                dtheta = 0
        
        theta += dtheta
        if theta<=0: theta = 1
        elif theta>=180: theta = 179
        # print(theta)
        
        # screen.blit(arrow, (arrow_x, arrow_y))
        rotated_arrow = pygame.transform.rotate(arrow, theta - 90)
        new_arrow_x = arrow_x + arrow.get_width()/2 - rotated_arrow.get_width()/2
        new_arrow_y = arrow_y + arrow.get_height()/2 - rotated_arrow.get_height()/2
        screen.blit(rotated_arrow, (new_arrow_x, new_arrow_y))
        # print(new_arrow_x, new_arrow_y)

        elapsed_time = pygame.time.get_ticks() - start_ticks
        falling_speed = random.randint(1500, 5000)
        step = prev_step + 1 if (prev_step + 1)==elapsed_time//falling_speed else prev_step
        if step>prev_step:
            hit = br.process_falling(bricks, SCREEN_WIDTH, SCREEN_HEIGHT)
            prev_step = step

        shooting_interval = 500
        shooting_step = prev_shooting_step + 1 if (prev_shooting_step + 1)==elapsed_time//shooting_interval else prev_shooting_step
        if shooting_step>prev_shooting_step:
            bullet = bu.Bullet(last_bullet_id + 1, GUN_POS, theta, bullet_speed)
            bullets[bullet.bullet_id] = bullet
            last_bullet_id = bullet.bullet_id
            prev_shooting_step = shooting_step
            # print(bullets)

        deleted_bullets = []
        for bullet in bullets.values():
            
            x, y = bullet.pos
            # print(x, y)
            dx = bullet.dx
            dy = bullet.dy
            x, y = x + dx, y - dy
            # print(x, y)
            if x<=0 or x>=SCREEN_WIDTH:
                dx = -1*dx
            if y<=2*BRICK_HEIGHT: # MUST BE MODIFIED
                dy = -1*dy
            
            if y>=SCREEN_HEIGHT:
                deleted_bullets.append(bullet.bullet_id)
                continue

            bullet.pos = (x, y)
            bullet.dx = dx
            bullet.dy = dy
            bullets[bullet.bullet_id] = bullet

            pygame.draw.circle(screen, bullet.color, bullet.pos, bullet.radius)

            prev_shooting_step = shooting_step
        
        for bullet_id in deleted_bullets:
            del(bullets[bullet_id])
        # print(bullets)

        score_render = score_font.render("SCORE : {}".format(elapsed_time//1000), True, BLACK)
        screen.blit(score_render, (180, BRICK_HEIGHT))

        for brick in bricks.values():
            pygame.draw.rect(screen, brick.color, brick.rect)
            hardness = hardness_font.render("{}".format(brick.hardness), True, WHITE)
            rect = brick.rect
            if brick.hardness < 10:
                hardness_pos = (rect[0] + rect[2]/2.5, rect[1] + rect[3]/3.5)
            else:
                hardness_pos = (rect[0] + rect[2]/3.5, rect[1] + rect[3]/3.5)
            screen.blit(hardness, hardness_pos)
              
        
        pygame.display.update()
        # pygame.time.delay(1000)
        # if hit: running = False

    pygame.time.delay(2000)
    pygame.quit()