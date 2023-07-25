import pygame

pygame.init()

# Basic parameters of the screen
WIDTH, HEIGHT = 900, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Pong")

clock = pygame.time.Clock()
FPS = 60

# Colors
BLACK = pygame.Color(0, 0, 0)
WHITE = pygame.Color(255, 255, 255)
GREEN = pygame.Color(0, 255, 0)
RED = pygame.Color(255, 0, 0)

# Font that is used to render the text
font20 = pygame.font.Font("freesansbold.ttf", 20)


class Striker:
    def __init__(self, posx, posy, width, height, speed, color):
        self._posx = posx
        self._posy = posy
        self.width = width
        self.height = height
        self.speed = speed
        self.color = color
        self.geek_rect = pygame.Rect(posx, posy, width, height)

    @property
    def posy(self):
        return self._posy

    @posy.setter
    def posy(self, value):
        self._posy = max(0, min(value, HEIGHT - self.height))
        self.geek_rect.y = self._posy

    def display(self):
        pygame.draw.rect(screen, self.color, self.geek_rect)

    def update(self, y_fac):
        self.posy += self.speed * y_fac

    def display_score(self, text, score, x, y, color):
        text = font20.render(text + str(score), True, color)
        text_rect = text.get_rect(center=(x, y))
        screen.blit(text, text_rect)

    def get_rect(self):
        return self.geek_rect


class Ball:
    def __init__(self, posx, posy, radius, speed, color):
        self.posx = posx
        self.posy = posy
        self.radius = radius
        self.speed = speed
        self.color = color
        self.x_fac = 1
        self.y_fac = -1
        self.ball = pygame.draw.circle(
            screen, self.color, (self.posx, self.posy), self.radius
        )
        self.first_time = True

    def display(self):
        self.ball = pygame.draw.circle(
            screen, self.color, (self.posx, self.posy), self.radius
        )

    def update(self):
        self.posx += self.speed * self.x_fac
        self.posy += self.speed * self.y_fac

        if self.posy <= 0 or self.posy >= HEIGHT:
            self.y_fac *= -1

        if self.posx <= 0 and self.first_time:
            self.first_time = False
            return -1
        elif self.posx >= WIDTH and self.first_time:
            self.first_time = False
            return 1
        else:
            return 0

    def reset(self):
        self.posx = WIDTH // 2
        self.posy = HEIGHT // 2
        self.x_fac *= -1
        self.first_time = True

    def hit(self):
        self.x_fac *= -1

    def get_rect(self):
        return self.ball


def main():
    running = True
    use_ball2 = False

    geek1 = Striker(20, 0, 10, 100, 10, GREEN)
    geek2 = Striker(WIDTH - 30, 0, 10, 100, 10, GREEN)
    ball = Ball(WIDTH // 2, HEIGHT // 2, 7, 3.5, WHITE)
    ball2 = Ball(WIDTH // 2, HEIGHT // 2, 7, 5, RED) if use_ball2 else None

    list_of_geeks = [geek1, geek2]
    geek1_score, geek2_score = 0, 0
    geek1_y_fac, geek2_y_fac = 0, 0

    while running:
        screen.fill(BLACK)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    geek2_y_fac = -1
                if event.key == pygame.K_DOWN:
                    geek2_y_fac = 1
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_UP or event.key == pygame.K_DOWN:
                    geek2_y_fac = 0

        for geek in list_of_geeks:
            if pygame.Rect.colliderect(ball.get_rect(), geek.get_rect()):
                ball.hit()
            if use_ball2 and pygame.Rect.colliderect(ball2.get_rect(), geek.get_rect()):
                ball2.hit()

        # AI PC
        if ball.posy > geek1.posy and abs(ball.posy - geek1.posy) > 10:
            geek1_y_fac = 1
        elif ball.posy < geek1.posy and abs(ball.posy - geek1.posy) > 10:
            geek1_y_fac = -1

        if use_ball2:
            if ball2.posy > geek1.posy and abs(ball2.posy - geek1.posy) > 10:
                geek1_y_fac = 1
            elif ball2.posy < geek1.posy and abs(ball2.posy - geek1.posy) > 10:
                geek1_y_fac = -1

        geek1.update(geek1_y_fac)
        geek2.update(geek2_y_fac)
        point1 = ball.update()
        point2 = ball2.update() if use_ball2 else None

        if point1 == -1:
            geek1_score += 1
        elif point1 == 1:
            geek2_score += 1

        if use_ball2 and point2:
            if point2 == -1:
                geek1_score += 1
            elif point2 == 1:
                geek2_score += 1

        if point1:
            ball.reset()
        if use_ball2 and point2:
            ball2.reset()

        geek1.display()
        geek2.display()
        ball.display()
        if use_ball2:
            ball2.display()

        geek1.display_score("Konstanz Gamer : ", geek1_score, 100, 20, WHITE)
        geek2.display_score("Collective Power : ", geek2_score, WIDTH - 100, 20, WHITE)

        pygame.display.update()
        clock.tick(FPS)


if __name__ == "__main__":
    main()
    pygame.quit()
