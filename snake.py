import pygame
from pygame.locals import *
from random import randint
import time

SCREEN_WIDTH=1000
SCREEN_HEIGHT=600

GREEN = (61, 153, 69)
WHITE = (255, 255, 255)

SIZE = 40

SPEED=0.1

class Apple:
    def __init__(self, main_screen):
        self.image = pygame.image.load("resources/apple.jpg")  # .convert()
        self.main_screen = main_screen
        self.x = SIZE * 3
        self.y = SIZE * 3

    def draw(self):
        self.main_screen.blit(self.image, (self.x, self.y))
        pygame.display.update()

    def move(self):
        self.x = randint(0, 24) * 40
        self.y = randint(0, 14) * 40
        pygame.display.update()


class Snake:
    def __init__(self, main_screen, length):
        self.length = length
        self.main_screen = main_screen
        self.block = pygame.image.load("resources/block.jpg")  # .convert()
        self.x = [SIZE] * length
        self.y = [SIZE] * length
        self.direction = "down"

    def increase_land(self):
        self.length += 1
        self.x.append(-1)
        self.y.append(-1)

    def draw(self):
        for i in range(self.length):
            self.main_screen.blit(self.block, (self.x[i], self.y[i]))
        pygame.display.update()

    def move_left(self):
        self.direction = "left"

    def move_right(self):
        self.direction = "right"

    def move_down(self):
        self.direction = "down"

    def move_up(self):
        self.direction = "up"

    def walk(self):

        for i in range(self.length - 1, 0, -1):
            self.x[i] = self.x[i - 1]
            self.y[i] = self.y[i - 1]

        if self.direction == "left":
            self.x[0] -= SIZE
        if self.direction == "right":
            self.x[0] += SIZE
        if self.direction == "up":
            self.y[0] -= SIZE
        if self.direction == "down":
            self.y[0] += SIZE

        self.draw()


class Game:
    def __init__(self):
        pygame.init()
        self.play_background_music()
        self.surface = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        # self.surface.fill(GREEN)
        self.snake = Snake(self.surface, 1)  #
        self.snake.draw()
        self.apple = Apple(self.surface)
        self.apple.draw()

    def is_collision(self, x1, y1, x2, y2):  # 1 is for snake, and 2 for apple
        if x1 >= x2 and x1 < x2 + SIZE:
            if y1 >= y2 and y1 < y2 + SIZE:
                return True
        return False

    def play_background_music(self):
        pygame.mixer.music.load("resources/bg_music_1.mp3")
        pygame.mixer.music.play()

    def play_sound(self, sound):
        sound = pygame.mixer.Sound(f"resources/1_snake_game_resources_{sound}.mp3")
        pygame.mixer.Sound.play(sound)

    def render_background(self):
        bg = pygame.image.load("resources/background.jpg")
        # pygame.transform.scale(bg,(1000,600))
        self.surface.blit(bg, (0, 0))

    def play(self):
        self.render_background()
        self.snake.walk()
        self.apple.draw()
        self.dispay_score()
        pygame.display.update()
        # snake collides with apple
        if self.is_collision(self.snake.x[0], self.snake.y[0],self.apple.x, self.apple.y):
            self.play_sound("ding")
            self.snake.increase_land()
            self.apple.move()

        # snake collides with itself
        for i in range(3, self.snake.length):
            if self.is_collision(self.snake.x[0], self.snake.y[0], self.snake.x[i], self.snake.y[i]):
                self.play_sound("crash")
                raise "Game over"

        #snake collides with the borders(screen edges)
        if self.snake.x[0]>=SCREEN_WIDTH or self.snake.y[0]>=SCREEN_HEIGHT or self.snake.x[0]<0 or self.snake.y[0]<0:
            self.play_sound("crash")
            raise "Game over"

    def show_game_over(self):
        self.render_background()
        font = pygame.font.SysFont("arial", 30)
        line1 = font.render(f"Game is over: Your score is {self.snake.length}", True, WHITE)
        self.surface.blit(line1, (200, 200))
        line2 = font.render("To play again press Enter! To exit press Escape!", True, WHITE)
        self.surface.blit(line2, (200, 250))

        pygame.display.update()

        pygame.mixer.music.pause()

    def dispay_score(self):
        font = pygame.font.SysFont("arial", 30)
        score = font.render(f"Score: {self.snake.length}", True, WHITE)
        self.surface.blit(score, (800, 10))

    def reset(self):
        self.snake = Snake(self.surface, 1)
        self.apple = Apple(self.surface)

    def run(self):
        running = True
        pause = False

        while running:
            for event in pygame.event.get():
                if event.type == KEYDOWN:
                    if event.key == K_ESCAPE:
                        running = False
                    if event.key == K_RETURN:
                        pygame.mixer.music.unpause()
                        pause = False
                    if event.key == K_LEFT:
                        self.snake.move_left()
                    if event.key == K_RIGHT:
                        self.snake.move_right()
                    if event.key == K_UP:
                        self.snake.move_up()
                    if event.key == K_DOWN:
                        self.snake.move_down()

                elif event.type == QUIT:
                    running = False
            try:
                if not pause:
                    self.play()
            except Exception as e:
                pause = True
                self.show_game_over()
                self.reset()
            time.sleep(SPEED)


def main():
    game = Game()
    game.run()

if __name__ == "__main__":
    main()
