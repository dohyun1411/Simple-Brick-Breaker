import os
import random
import pygame
import brick as br
import bullet as bu
# import collision_checker as cc


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
    game_over_font = pygame.font.Font(None, 50)
    
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
    bullet_speed = 0.3
    # falling_speed = random.randint(1500, 5000)
    falling_speed = 1500
    shooting_interval = 700
    radius = 5
    GUN_RECT = (220, 600, 40, 40)
    GUN_WIDTH = 3
    GUN_POS = (240, 620)
    arrow_x, arrow_y = 237.5, 605
    speed_up_count = 0
    speed_up = False
    hit = False
    last_score = 0

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
        step = prev_step + 1 if (prev_step + 1)==elapsed_time//falling_speed else prev_step
        if step>prev_step:
            hit = br.process_falling(bricks, SCREEN_WIDTH, SCREEN_HEIGHT)
            prev_step = step

        score = elapsed_time//1000
        score_render = score_font.render("SCORE : {}".format(score), True, BLACK)
        screen.blit(score_render, (180, BRICK_HEIGHT))


        # print(speed_up)
        # if not speed_up and random.random() < 0.01: speed_up = True
        # speed_up = True
        # if speed_up:
        #     if score > last_score: speed_up_count += 1
        #     shooting_interval = 350
        #     item_msg = score_font.render("Speed Up", True, (255, 153, 51))
        #     item_msg_rect = item_msg.get_rect(center=(int(SCREEN_WIDTH/2), int(SCREEN_HEIGHT - 2*BRICK_HEIGHT)))
        #     screen.blit(item_msg, item_msg_rect)
        #     last_score = score
        #     if speed_up_count > 5:
        #         shooting_interval = 700
        #         speed_up = False

        # if 2 <= score <= 7:
        #     shooting_interval = 350
        # else:
        #     shooting_interval = 700
        
        shooting_step = prev_shooting_step + 1 if (prev_shooting_step + 1)==elapsed_time//shooting_interval else prev_shooting_step
        # print(shooting_step, prev_shooting_step, elapsed_time//shooting_interval)

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
            if y<=2*BRICK_HEIGHT:
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
            try:
                del(bullets[bullet_id])
            except KeyError:
                pass
        # print(bullets)


        deleted_bricks = []
        for brick in bricks.values():
            
            brick_rect = pygame.Rect(*brick.rect)
            for bullet in bullets.values():
                left = bullet.pos[0] - bullet.radius
                top = bullet.pos[1] - bullet.radius
                bullet_rect = pygame.Rect(left, top, 2*bullet.radius, 2*bullet.radius)

                # threshold = 10
                if brick_rect.colliderect(bullet_rect):
                    # print("COLLISION")
                    # print(brick.rect)
                    # print(bullet.pos)
                    # pygame.time.delay(1000)
                    
                    a = abs(bullet_rect.left - (brick_rect.left + brick_rect.width))
                    b = abs((bullet_rect.left + bullet_rect.width) - brick_rect.left)
                    c = abs(bullet_rect.top - (brick_rect.top + brick_rect.height))
                    d = abs((bullet_rect.top + bullet_rect.height) - brick_rect.top)

                    left_collision = min(a, b)
                    top_collision = min(c, d)
                    # print(a, b, c, d)
                    if left_collision < top_collision:
                        # print("dx")
                        bullet.dx = -1*bullet.dx
                    else:
                        # print("dy")
                        bullet.dy = -1*bullet.dy
                    
                    # print(abs(bullet_rect.left - (brick_rect.left + brick_rect.width)), abs((bullet_rect.left + bullet_rect.right) -brick_rect.left), abs(bullet_rect.top - (brick_rect.top + brick_rect.height)), abs((bullet_rect.top + bullet_rect.height) -brick_rect.top))



                # collision_checker = cc.collision_checker(brick.rect, (bullet.pos, bullet.radius))
                # # if collision_checker: print(collision_checker)
                # if collision_checker == 1: bullet.dy = -1*dy
                # elif collision_checker ==2: bullet.dx = -1*dx
                # else: continue
                
                    bullets[bullet.bullet_id] = bullet


                    brick.hardness -= 1
                    # brick.hardness = 0
                    if brick.hardness<=0:
                        deleted_bricks.append(brick.brick_id)
                        continue




            pygame.draw.rect(screen, brick.color, brick.rect)
            hardness = hardness_font.render("{}".format(brick.hardness), True, WHITE)
            rect = brick.rect
            if brick.hardness < 10:
                hardness_pos = (rect[0] + rect[2]/2.5, rect[1] + rect[3]/3.5)
            else:
                hardness_pos = (rect[0] + rect[2]/3.5, rect[1] + rect[3]/3.5)
            screen.blit(hardness, hardness_pos)
        
        for brick_id in deleted_bricks:
            try:
                del(bricks[brick_id])
            except:
                pass           

        
        pygame.display.update()
        if hit: running = False


    msg = game_over_font.render("Game Over", True, BLACK)
    msg_rect = msg.get_rect(center=(int(SCREEN_WIDTH/2), int(SCREEN_HEIGHT/2)))
    screen.blit(msg, msg_rect)

    new_record = False
    with open("score.txt", 'r') as f:
        best_score = int(f.read())
        # print(best_score)
        if score > best_score:
            score_msg = game_over_font.render("<New Record>", True, (255, 153, 51))
            score_msg_rect = score_msg.get_rect(center=(int(SCREEN_WIDTH/2), int(SCREEN_HEIGHT/2 - 60)))
            screen.blit(score_msg, score_msg_rect)
            new_record = True

    pygame.display.update()
    
    if new_record:
        with open("score.txt", 'w') as f:
            f.write("{}".format(score))

    pygame.time.delay(3000)
    pygame.quit()