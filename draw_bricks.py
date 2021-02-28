import os
import pygame
import brick as br


if __name__=="__main__":

    pygame.init()

    SCREEN_WIDTH = 480
    SCREEN_HEIGHT = 640
    WHITE = (255, 255, 255)
    BLACK = (0, 0, 0)

    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    screen.fill(WHITE)

    hardness_font = pygame.font.Font(None, 25)
    
    pygame.display.set_caption("swipe_brick_breaker")

    
    running = True
    bricks = {}
    start_ticks = pygame.time.get_ticks()
    prev_step = 0
    while running:

        for event in pygame.event.get():
            if event.type==pygame.QUIT:
                running = False
        
        elapsed_time = pygame.time.get_ticks() - start_ticks
        step = prev_step + 1 if (prev_step + 1)==elapsed_time//1000 else prev_step
        if step>prev_step:
            prev_step = step
            screen.fill(WHITE)
            hit = br.process_falling(bricks, SCREEN_WIDTH, SCREEN_HEIGHT)

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


    pygame.time.delay(2000)
    pygame.quit()