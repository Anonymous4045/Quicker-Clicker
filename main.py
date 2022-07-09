import pygame

WIDTH, HEIGHT = 1000, 800

pygame.init()
pygame.font.init()

# Assets
sprites = []

pygame.display.set_caption('Quicker Clicker')

screen = pygame.display.set_mode((WIDTH, HEIGHT))

# Colors
white = 255, 255, 255
black = 0, 0, 0
red = 255, 0, 0
green = 0, 255, 0
blue = 0, 0, 255


point_in_rect = lambda point, rect: rect.collidepoint(point)


class Button:
    def __init__(self,name,message,foreground,background,size,x,y):
        self.name = name
        self.message = message
        self.foreground = foreground
        font = pygame.font.get_default_font()
        self.text = pygame.font.Font(font, size).render(message, True, foreground, background)
        self.rect = self.text.get_rect()
        self.rect.center = x, y

    def outline(self):
        pygame.draw.rect(screen, self.foreground, self.rect, 1)


class Text:
    def __init__(self, name, message, foreground, background, size, x, y):
        self.name = name
        self.message = message
        self.foreground = foreground
        font = pygame.font.get_default_font()
        self.text = pygame.font.Font(font, size).render(message, True, foreground, background)
        self.rect = self.text.get_rect()
        self.rect.center = x, y


title = Text('title', 'Quicker Clicker', white, black, 100, 500, 300)
sprites.append(title)
play_button = Button('play_button', 'Play', white, black, 64, 500, 400)
sprites.append(play_button)


def show(sprites):
    for sprite in sprites:
        screen.blit(sprite.text,sprite.rect)
        if isinstance(sprite,Button):
            sprite.outline()


menu = True
while menu:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            print('Menu closed')
            pygame.quit()
            quit()
            exit(0)

        elif event.type == pygame.MOUSEBUTTONDOWN:
            for sprite in sprites:
                if isinstance(sprite, Button):
                    if point_in_rect(event.pos, sprite.rect):
                        menu = False

    screen.fill(black)

    show(sprites)

    pygame.display.update()

sprites = []


score_display = lambda score: Text('score_display', 'Score: {:,}'.format(score), white, black, 64, WIDTH // 2, 32)
sprites.append(score_display(0))
rebirths_display = lambda rebirths: Text('rebirths_display', f"Rebirths: {rebirths}", white, black, 64, WIDTH // 2, 96)
sprites.append(rebirths_display(0))
prestige_display = lambda prestige: Text('prestige_display',f"Prestiges: {prestige}", white, black, 64, WIDTH // 2, 160)
sprites.append(rebirths_display(0))

upgrade = lambda cost: Button('upgrade', 'Upgrade: {:,}'.format(cost), green, black, 50, WIDTH // 2, 250)
sprites.append(upgrade(25))
rebirth = lambda cost: Button('rebirth', 'Rebirth: {:,}'.format(cost), red, black, 50, WIDTH // 2, 325)
sprites.append(rebirth(1000))
prestige = lambda cost: Button('prestige', 'Prestige: {:,}'.format(cost), white, black, 50, WIDTH // 2, 400)
sprites.append(prestige(0))

score = rebirths = prestiges = 0
increase = 1
upgrade_cost, rebirth_cost, prestige_cost = 25, 1_000, 1_000_000

game_loop = True
while game_loop:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            print('Game closed')
            pygame.quit()
            quit()
            exit(0)
        elif event.type == pygame.MOUSEBUTTONDOWN:
            score += increase + prestiges * 10
            for sprite in sprites:
                if isinstance(sprite, Button):
                    if point_in_rect(event.pos, sprite.rect):
                        if sprite.name == 'upgrade':
                            if score >= upgrade_cost:
                                score = 0
                                increase *= 3 + rebirths * 2
                                upgrade_cost *= 5 * rebirths if rebirths > 0 else 5
                        elif sprite.name == 'rebirth':
                            if score >= rebirth_cost:
                                score = 0
                                increase = 1
                                upgrade_cost = 25
                                rebirths += 1
                                rebirth_cost *= 10
                        elif sprite.name == 'prestige':
                            if score > prestige_cost:
                                prestige_cost *= 10
                                score = rebirths = 0
                                prestiges += 1
                                increase = 1
                                rebirth_cost = 1000
                                upgrade_cost = 25

    screen.fill(black)

    sprites = [prestige_display(prestiges), prestige(prestige_cost), rebirths_display(rebirths), score_display(score), upgrade(upgrade_cost), rebirth(rebirth_cost)]
    show(sprites)

    pygame.display.update()
