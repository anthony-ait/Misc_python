import pygame
import os
import random
import button 

#function to count number of files in a directory
def count_files_in_directory(directory_path):
    return len([f for f in os.listdir(directory_path) if os.path.isfile(os.path.join(directory_path, f))])


pygame.init()
clock = pygame.time.Clock()
fps = 60


#game music
# Create a list of music files to play
music_files = ["music/battle_theme.mp3"]

# Load the first song in the list
current_song_index = 0
pygame.mixer.music.load(music_files[current_song_index])
pygame.mixer.music.set_volume(0.5)

#game sound
heal_sound = pygame.mixer.Sound("sound/heal.wav")
confirm_sound = pygame.mixer.Sound("sound/confirm.wav")
slash_sound = pygame.mixer.Sound("sound/slash.wav")
slash_sound.set_volume(0.5)
death_sound = pygame.mixer.Sound("sound/death.wav")


#game window
bottom_panel = 150
screen_width = 800
screen_height = 400 + bottom_panel

screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption('Battle')

#define game variables
current_fighter = 1
total_fighters = 3
action_cooldown = 0
action_wait_time = 90
attack = False
potion = False
potion_effect = 15
target = None
clicked = False
game_over = 0

#defini fonts
font = pygame.font.SysFont('MinimalPixel2', 26)

#define colours
red = (255, 0, 0)
green = (0, 255, 0)


#load images
#background images
background_img = pygame.image.load('image/Background/background.png').convert_alpha()
#panel image
panel_img = pygame.image.load('image/Icons/panel.png').convert_alpha()
#button images
potion_img = pygame.image.load('image/Icons/potion.png').convert_alpha()
restart_img = pygame.image.load('image/Icons/restart.png').convert_alpha()

#victory and defeat images
victory_img = pygame.image.load('image/Icons/victory.png').convert_alpha()
defeat_img = pygame.image.load('image/Icons/defeat.png').convert_alpha()

#sword image
sword_img = pygame.image.load('image/Icons/sword.png').convert_alpha()


#origin is on the up left (x positive to the right and y postive down)

#create function for drawing text
def draw_text(text, font, text_col, x, y):
    img = font.render(text, True, text_col)
    screen.blit(img, (x, y))


#function for drawing background
def draw_background():
    screen.blit(background_img, (0,0))

#function for drawing panel
def draw_panel():
    #draw panel rectangle
    screen.blit(panel_img, (0,screen_height - bottom_panel))
    #show knight stats
    draw_text(f'{knight.name} HP : {knight.hp}' ,font, red, 100, screen_height - bottom_panel + 10)
    for count, i in enumerate(bandit_list):
        #show name and health
         draw_text(f'{i.name} HP : {i.hp}' ,font, red, 550, (screen_height - bottom_panel + 10) + count * 60 )



#fighter class
class Fighter():
    def __init__(self, x, y, name, max_hp, strength, potions):
        self.name = name
        self.max_hp = max_hp
        self.hp = max_hp
        self.strength = strength
        self.start_potions = potions
        self.potions = potions
        self.alive = True
        self.animation_list = {'Idle':[], 'Attack':[], 'Hurt':[], 'Death':[]}
        self.frame_index = 0 #choose which frame of image to put when I run
        self.action = 'Idle' 
        self.update_time = pygame.time.get_ticks()
        #load images
        for key in self.animation_list:
            temp_list=[]
            directory_path = f'image/{self.name}/{key}' #take name of Fighter to take good image
            number_of_files = count_files_in_directory(directory_path)
            print(number_of_files)
            for i in range(number_of_files):
                img = pygame.image.load(f'{directory_path}/{i}.png') 
                img = pygame.transform.scale(img, (img.get_width() * 3, img.get_height() * 3))
                temp_list.append(img)
            self.animation_list[key] = temp_list
        self.image = self.animation_list[self.action][self.frame_index]
        self.rect = self.image.get_rect() #take width and height of picture
        self.rect.center = (x,y)

    def update(self):
        animation_cooldown = 100
        #handle animation
        #update image
        self.image = self.animation_list[self.action][self.frame_index]
        #check if enough time has passed sinced the last update
        if pygame.time.get_ticks() - self.update_time > animation_cooldown:
            self.update_time = pygame.time.get_ticks()
            self.frame_index += 1
        #if the animation has run out then reset back to Idle
        if self.frame_index >= len(self.animation_list[self.action]):
            if self.action == 'Death':
                self.frame_index = len(self.animation_list[self.action]) - 1
            else:
                self.idle()

    def idle(self):
        #set variables to idle animation
        self.action = 'Idle'
        self.frame_index = 0
        self.update_time = pygame.time.get_ticks()


    def attack(self, target):
        #deal damage to enemy
        rand = random.randint(-5, 5)
        damage = self.strength + rand
        pygame.mixer.Sound.play(slash_sound)
        target.hp -= damage
        target.hurt()
        #check if target has died
        if target.hp < 1:
            target.hp = 0
            target.alive = False
            target.death()
        damage_text = DamageText(target.rect.centerx, target.rect.y, str(damage), red)
        damage_text_group.add(damage_text)
        #set variables to attack animation
        self.action = 'Attack'
        self.frame_index = 0
        self.update_time = pygame.time.get_ticks()

    def hurt(self):
        #set variables to hurt animation
        self.action = 'Hurt'
        self.frame_index = 0
        self.update_time = pygame.time.get_ticks()

    def death(self):
        #set variables to hurt animation
        pygame.mixer.Sound.play(death_sound)
        self.action = 'Death'
        self.frame_index = 0
        self.update_time = pygame.time.get_ticks()


    def reset(self):
        self.alive = True
        self.potions = self.start_potions
        self.hp = self.max_hp
        self.frame_index = 0
        self.action = 'Idle'
        self.update_time = pygame.time.get_ticks()

     
    def draw(self):
        screen.blit(self.image, self.rect)
    
class HealthBar():
    def __init__(self, x, y, hp, max_hp):
        self.x = x
        self.y = y
        self.hp = hp
        self.max_hp = max_hp
    
    def draw(self, hp):
        #update hp
        self.hp = hp
        #calculate health ratio
        ratio = self.hp/self.max_hp
        pygame.draw.rect(screen, red, (self.x, self.y, 150, 20))
        pygame.draw.rect(screen, green, (self.x, self.y, 150*ratio, 20))

class DamageText(pygame.sprite.Sprite):
    def __init__(self, x, y, damage, colour):
        pygame.sprite.Sprite.__init__(self)
        self.image = font.render(damage, True, colour)
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.counter = 0

    def update(self):
        #move damage text up
        self.rect.y -= 1
        #delete the text after a few seconds
        self.counter += 1
        if self.counter > 30:
            #delete text
            self.kill()



damage_text_group = pygame.sprite.Group()


knight = Fighter(200, 260, 'Knight', 30, 10, 3)

bandit1 = Fighter(500, 270, 'Necromancer', 20, 6, 1)
bandit2 = Fighter(700, 270, 'Bandit', 20, 6, 3)

bandit_list = []
bandit_list.append(bandit1)
bandit_list.append(bandit2)

knight_health_bar = HealthBar(100, screen_height - bottom_panel + 40, knight.hp, knight.max_hp)
bandit1_health_bar = HealthBar(550, screen_height - bottom_panel + 40, bandit1.hp, bandit1.max_hp)
bandit2_health_bar = HealthBar(550, screen_height - bottom_panel + 100, bandit2.hp, bandit2.max_hp)

#create buttons
potion_button = button.Button(screen, 100, screen_height - bottom_panel + 70, potion_img, 64, 64)
restart_button = button.Button(screen, 330, 120, restart_img, 120, 30)

run = True 
# Play the current song
pygame.mixer.music.play()
while run:

    #set fps for game
    clock.tick(fps)

    #draw background
    draw_background()

    #draw panel
    draw_panel()
    knight_health_bar.draw(knight.hp)
    bandit1_health_bar.draw(bandit1.hp)
    bandit2_health_bar.draw(bandit2.hp)

    #draw Fighters
    #draw knight
    knight.update()
    knight.draw()

    #draw bandit
    for bandit in bandit_list:
        bandit.update()
        bandit.draw()

    #draw the damage text
    damage_text_group.update()
    damage_text_group.draw(screen)



    #control player actions
    #reset action variables
    attack = False
    potion = False
    target = None
    #make sure mouse is visible
    pygame.mouse.set_visible(True)

    #show sword if go on bandit
    pos = pygame.mouse.get_pos()
    for count, bandit in enumerate(bandit_list):
        if bandit.rect.collidepoint(pos):
            #hide mouse
            pygame.mouse.set_visible(False)
            #show sword instead of mouse cursor
            screen.blit(sword_img, pos)
            if clicked and bandit.alive:
                attack = True
                target = bandit

    if potion_button.draw():
        potion = True
    #show number of potions remaining
    draw_text(str(knight.potions), font, red, 150, screen_height - bottom_panel +70)

    if game_over ==0:
        #player action
        if knight.alive :
            if current_fighter == 1:
                action_cooldown += 1
                if action_cooldown >= action_wait_time:
                    #look for player action
                    #attack
                    if attack == True and target != None:
                        knight.attack(target)
                        current_fighter += 1
                        action_cooldown = 0
                    #heal
                    if potion == True:
                        if knight.potions > 0:
                            #make sure we don't heal beyon max hp
                            heal_amount = min(potion_effect, knight.max_hp - knight.hp)
                            pygame.mixer.Sound.play(heal_sound)
                            knight.hp += heal_amount
                            damage_text = DamageText(knight.rect.centerx, knight.rect.y, str(heal_amount), green)
                            damage_text_group.add(damage_text)
                            knight.potions -= 1
                            current_fighter += 1
                            action_cooldown = 0
        else : 
            game_over = -1


        #enemy action
        for count, bandit in enumerate(bandit_list):
            if current_fighter == 2 + count:
                if bandit.alive:
                    action_cooldown +=1
                    if action_cooldown >= action_wait_time:
                        #check if bandit need to heal first
                        if (bandit.hp / bandit.max_hp) < 0.5 and bandit.potions > 0:
                            #heeal
                            heal_amount = min(potion_effect, bandit.max_hp - bandit.hp)
                            pygame.mixer.Sound.play(heal_sound)
                            bandit.hp += heal_amount
                            damage_text = DamageText(bandit.rect.centerx, bandit.rect.y, str(heal_amount), green)
                            damage_text_group.add(damage_text)
                            bandit.potions -= 1
                            current_fighter += 1
                            action_cooldown = 0   
                        else:                    
                            #attack
                            bandit.attack(knight)
                            current_fighter += 1
                            action_cooldown = 0
                else:
                    current_fighter += 1

        #check if all fighters have had a turn then reset
        if current_fighter > total_fighters:
            current_fighter = 1
    
    #check if all bandits are dead
    alive_bandits = 0
    for bandit in bandit_list:
        if bandit.alive:
            alive_bandits += 1
    if alive_bandits == 0:
        game_over =1

    #check if game is over
    if game_over != 0:
        if game_over == 1:
            screen.blit(victory_img, (250, 50))
        if game_over == -1:
            screen.blit(defeat_img, (250, 50))
        if restart_button.draw():
            pygame.mixer.Sound.play(confirm_sound)
            knight.reset()
            for bandit in bandit_list:
                bandit.reset()
            current_fighter = 1
            action_cooldown = 0
            game_over = 0    

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            clicked = True
        else:
            clicked = False

    pygame.display.update()

pygame.quit()