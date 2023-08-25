import pygame
from sys import exit
from random import randint
pygame.init()

def display_score():
     current_time = pygame.time.get_ticks() - start_time
     score_surf = test_font.render(f'Score: {int(current_time/1000)}',False,(64,64,64))
     score_rect = score_surf.get_rect(center = (400,50))
     screen.blit(score_surf,score_rect)
     return int(current_time/1000)
def obstacle_movement(obstacle_list):
    if obstacle_list:
        for obstacle_rect in obstacle_list:
            obstacle_rect.x -= 5.5
            if obstacle_rect.bottom == 300:
                screen.blit(snail_surf,obstacle_rect)
            else:
                screen.blit(fly_surf,obstacle_rect)
        obstacle_list = [obs for obs in obstacle_list if obs.x>-100]
        return obstacle_list
    else:
        return []
def collision(player,obstacles):
    if obstacles:
        for obstacles_rect in obstacles:
            if player.colliderect(obstacles_rect):
                end_sound = pygame.mixer.Sound('Audio/game_over.mp3')
                end_sound.play()
                return False
    return True
def player_animation():
    global player_surf, player_index
    if player_rect.bottom<300:
        player_surf = player_jump
    else:
        player_index += 0.1
        if player_index>= len(player_walk):
            player_index = 0
        player_surf = player_walk[int(player_index)]
screen = pygame.display.set_mode((800,400))
pygame.display.set_caption('Runner')
clock = pygame.time.Clock()
test_font = pygame.font.Font('font/Pixeltype.ttf',50)
game_active = False
start_time = 0
score = display_score()

sky_surface = pygame.image.load('graphics/Sky.png').convert_alpha()
ground_surface = pygame.image.load('graphics/ground.png').convert_alpha()

#obstacles
snail_frame1 = pygame.image.load('graphics/snail1.png').convert_alpha()
snail_frame2 = pygame.image.load('graphics/snail2.png').convert_alpha()
snail_frames = [snail_frame1,snail_frame2]
snail_frame_index = 0
snail_surf = snail_frames[snail_frame_index]

fly_frame1 = pygame.image.load('graphics/Fly1.png').convert_alpha()
fly_frame2 = pygame.image.load('graphics/Fly2.png').convert_alpha()
fly_frames = [fly_frame1,fly_frame2]
fly_frame_index = 0
fly_surf = fly_frames[fly_frame_index]

obstacle_rect_list = []

#player
player_walk_1 = pygame.image.load('graphics/player_walk_1.png').convert_alpha()
player_walk_2 = pygame.image.load('graphics/player_walk_2.png').convert_alpha()
player_walk = [player_walk_1 , player_walk_2]
player_index = 0
player_jump_sound = pygame.mixer.Sound('Audio/jump.mp3')
player_jump = pygame.image.load('graphics/jump.png').convert_alpha()
player_surf = player_walk[player_index]
player_rect = player_surf.get_rect(midbottom = (80,300))
player_gravity = 0

#intro
player_stand = pygame.image.load('graphics/player_stand.png').convert_alpha()
player_stand = pygame.transform.rotozoom(player_stand,0,2)
player_stand_rect = player_stand.get_rect(center = (400,200))
game_name = test_font.render('Pixel Runner' , False , (111,196,169))
name_rect = game_name.get_rect(center = (400,80))
game_strt = test_font.render('Press space to run!' , False, (111,196,169))
strt_rect = game_strt.get_rect(center = (400,320))

#timer
obstacle_timer = pygame.USEREVENT + 1
pygame.time.set_timer(obstacle_timer,1600)

snail_annimation_timer = pygame.USEREVENT + 2
pygame.time.set_timer(snail_annimation_timer,500)

fly_annimation_timer = pygame.USEREVENT + 3
pygame.time.set_timer(fly_annimation_timer,200)

while True:

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()
        if game_active:
            if event.type == pygame.MOUSEBUTTONUP:
                if player_rect.collidepoint(event.pos) and player_rect.bottom >=300:
                    player_gravity = -20
            if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE and player_rect.bottom >=300:
                        player_gravity = -20
                        player_jump_sound.play()
        else:
             if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE :
                        game_active = True
                        start_time = pygame.time.get_ticks()

        if game_active:
            if event.type == obstacle_timer:
                if randint(0,2):
                    obstacle_rect_list.append(snail_surf.get_rect(midbottom = (randint(900,1100),300)))
                else:
                    obstacle_rect_list.append(fly_surf.get_rect(midbottom = (randint(900,1100),210)))
            if event.type == snail_annimation_timer:
                if snail_frame_index == 0:
                    snail_frame_index = 1
                else:
                    snail_frame_index = 0
                snail_surf = snail_frames[snail_frame_index]

            if event.type == fly_annimation_timer:
                if fly_frame_index == 0:
                    fly_frame_index = 1
                else:
                    fly_frame_index = 0
                fly_surf = fly_frames[fly_frame_index]


    if game_active == True:
        screen.blit(sky_surface,(0,0))
        screen.blit(ground_surface,(0,300))
        score = display_score()
        display_score()
        
        
        #player
        player_gravity += 1
        player_rect.bottom += player_gravity
        if player_rect.bottom >=300:
            player_rect.bottom = 300
        player_animation()
        screen.blit(player_surf,player_rect)

        #obstacle movement
        obstacle_rect_list = obstacle_movement(obstacle_rect_list)
        #collisions
        game_active = collision(player_rect,obstacle_rect_list)

    else:
        screen.fill((94,129,162))
        screen.blit(player_stand,player_stand_rect)
        screen.blit(game_name,name_rect)
        obstacle_rect_list.clear()
        player_rect.midbottom = (80,300)
        player_gravity = 0
        score_msg = test_font.render(f'Your Score : {score}' ,False,(111,196,169))
        score_msg_rect = score_msg.get_rect(center = (400,330))
        if score == 0:
            screen.blit(game_strt,strt_rect)
        else:
            screen.blit(score_msg,score_msg_rect)

    pygame.display.update()
    clock.tick(1)

    