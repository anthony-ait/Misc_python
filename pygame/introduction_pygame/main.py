import pygame

pygame.init()

screen_width = 800
screen_height = 400

fps = 60

screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption('Runner')

clock = pygame.time.Clock()



run = True

while run:
    pygame.display.update()
    clock.tick(fps)

    




    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False



    





pygame.quit()