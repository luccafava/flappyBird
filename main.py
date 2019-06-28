import random, pygame, sys
from pygame.locals import *
from bird import Bird
from pipe import Pipe
from scorecounter import ScoreCounter

pygame.init()
screen_info = pygame.display.Info()

size = (width, height) = (int(screen_info.current_w), int(screen_info.current_h))
screen = pygame.display.set_mode(size)

clock = pygame.time.Clock()

background = pygame.image.load('background.png')
background = pygame.transform.scale(background, (width, height))

color = (255, 0, 0)

scorecounters = pygame.sprite.Group()

startPos = (width/8, height/2)
pipes = pygame.sprite.Group()
player = Bird(startPos)
gapSize = 200
loopCount = 0
score = 0
gamePlay = True

def lose():
    global score, gamePlay
    score = 0
    font = pygame.font.SysFont(None, 70)
    text = font.render("You died!", True, (0, 0, 255))
    text_rect = text.get_rect()
    text_rect.center = (width/2, height/2)
    while True:
        screen.fill(color)
        screen.blit(text, text_rect)
        pygame.display.flip()
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    scorecounters.empty()
                    pipes.empty()
                    player.reset(startPos)
                    return

def displayScore(score):
    font = pygame.font.SysFont(None, 70)
    text = font.render("Score:" + str(score), True, (255, 0, 0))
    text_rect = text.get_rect()
    text_rect.center = (width/2, height/2)
    screen.blit(text, text_rect)

def main():
    global loopCount, score
    while True:
        clock.tick(60)
        if loopCount % 90 == 0:
            topPos = random.randint(0, height/2) - 400
            pipes.add(Pipe((width + 100, topPos + gapSize + 800)))
            pipes.add(Pipe((width + 100, topPos), True))
            scorecounters.add(ScoreCounter((width + 100, 0)))
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    player.speed[1] = -10
        player.update()
        pipes.update()
        gets_hit = pygame.sprite.spritecollide(player, pipes, False) \
            or player.rect.center[1] > height
        screen.blit(background, [0,0])
        pipes.draw(screen)
        screen.blit(player.image, player.rect)
        pygame.display.flip()
        loopCount += 1

        scorecounters.update()
        score_counters_hit = pygame.sprite.spritecollide(player, scorecounters, False)

        if score_counters_hit.__len__() > 0:
            score += 1
            scorecounters.remove(score_counters_hit)
        scorecounters.draw(screen)
        displayScore(score)

        if gets_hit:
            lose()


if __name__ == '__main__':
    main()