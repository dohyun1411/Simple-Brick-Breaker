import os
import random
import pygame
import brick as br


if __name__=="__main__":

    pygame.init()

    SCREEN_WIDTH = 480
    SCREEN_HEIGHT = 640
    BRICK_WIDTH = 40
    BRICK_HEIGHT = 40
    WHITE = (255, 255, 255)
    BLACK = (0, 0, 0)

    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    screen.fill(WHITE)

    hardness_font = pygame.font.Font(None, 25)
    score_font = pygame.font.Font(None, 30)
    
    pygame.display.set_caption("swipe_brick_breaker")

    
    running = True
    bricks = {}
    start_ticks = pygame.time.get_ticks()
    prev_step = 0
    theta = 90
    dtheta = 0
    angular_speed = 5
    while running:

        for event in pygame.event.get():
            if event.type==pygame.QUIT: running = False

            if event.type==pygame.KEYDOWN:
                if event.key==pygame.K_LEFT:
                    dtheta -= angular_speed
                if event.key==pygame.K_RIGHT:
                    dtheta += angular_speed
            
            if event.type==pygame.KEYUP:
                dtheta = 0
        
        theta += dtheta
        if theta<0: theta = 0
        elif theta>90: theta = 90


        


        
        elapsed_time = pygame.time.get_ticks() - start_ticks
        falling_speed = random.randint(1500, 5000)
        step = prev_step + 1 if (prev_step + 1)==elapsed_time//falling_speed else prev_step

        screen.fill(WHITE)
        if step>prev_step:
            hit = br.process_falling(bricks, SCREEN_WIDTH, SCREEN_HEIGHT)
            prev_step = step

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