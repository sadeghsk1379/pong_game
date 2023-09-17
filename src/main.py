""".

Pong Game

This module implements a simple Pong game using the Pygame library.

Author: Sadegh Sargazi

"""
import random
import sys

import pygame


class Player:
    """.

    Create a player for the game

    """

    def __init__(
        self,
        name: str,
        roll: str,
        speed: int,
        placement: str,
    ) -> None:
        """.

        In init we need to create some varibles for out player

        """
        self.name = name
        self.roll = roll
        self.speed = speed
        self.score = 0
        self.text = ""

        if placement == "Home":
            self.placement = pygame.Rect(10, SCREEN_WIDTH / 2 - 70, 10, 140)

        else:
            self.placement = pygame.Rect(
                SCREEN_WIDTH - 20,
                SCREEN_WIDTH / 2 - 70,
                10,
                140,
            )

            self.placement = pygame.Rect(
                SCREEN_WIDTH - 20,
                SCREEN_WIDTH / 2 - 70,
                10,
                140,
            )

    def player_animation(self, screen_height):
        """.

        in this function we create movement for our user

        """
        self.placement.y += self.speed

        self.placement.top = max(self.placement.top, 0)

        self.placement.bottom = min(self.placement.bottom, screen_height)

    def opponent_cpu(self, screen_height, ball_cpu):
        """.

        we create a cpu for offline mode

        """
        if self.placement.top < ball_cpu.place.y:
            self.placement.top += self.speed

        if self.placement.bottom > ball_cpu.place.y:
            self.placement.bottom -= self.speed

        self.placement.top = max(self.placement.top, 0)

        self.placement.bottom = min(self.placement.bottom, screen_height)


class Ball:
    """.

    in this class we can create some balls for our game

    """

    def __init__(self, name, speed_x, speed_y) -> None:
        """.

        In init we create speed and animation for our ball

        """
        if name == "1":
            self.name = name
            self.speed_x = speed_x * random.choice((1, -1))
            self.speed_y = speed_y * random.choice((1, -1))
            self.place = pygame.Rect(
                SCREEN_WIDTH / 2 - 15,
                SCREEN_HEIGHT / 2 - 15,
                30,
                30,
            )

            self.score_time = 0
            self.score_check = True

    def ball_animation(self, player_home, cpu, screen_width, screen_height):
        """.

        in this function we move the ball in diffrent directions

        """
        self.place.x += self.speed_x
        self.place.y += self.speed_y

        if self.place.top <= 0 or self.place.bottom >= screen_height:
            self.speed_y *= -1

        if self.place.left <= 0:
            pygame.mixer.Sound.play(Score_Sound)

            player_home.score += 1

            self.score_time = pygame.time.get_ticks()
            self.score_check = True

        if self.place.right >= screen_width:
            pygame.mixer.Sound.play(Score_Sound)

            cpu.score += 1

            self.score_time = pygame.time.get_ticks()

            self.score_check = True

        if self.place.colliderect(Cpu.placement) and self.speed_x > 0:
            if abs(self.place.right - Cpu.placement.left) < 10:
                self.speed_x *= -1

            bottom_diff = abs(self.place.bottom - Cpu.placement.top)
            if 0 < bottom_diff < 10 < self.speed_y:
                self.speed_y *= -1

            top_diff = abs(self.place.top - Cpu.placement.bottom)
            if self.speed_y < 0 < top_diff < 10:
                self.speed_y *= -1

        if self.place.colliderect(Player_Home.placement) and self.speed_x < 0:
            if abs(self.place.left - Player_Home.placement.right) < 10:
                self.speed_x *= -1

            bottom_diff = abs(self.place.bottom - Player_Home.placement.top)
            if 0 < bottom_diff < 10 < self.speed_y:
                self.speed_y *= -1

            elif (
                abs(self.place.top - Player_Home.placement.bottom) < 10
                and self.speed_y < 0
            ):
                self.speed_y *= -1

    def ball_restart(self, screen_width, screen_height):
        """.

        In this function we place the ball to the center after scoring a goal

        """
        current_time = pygame.time.get_ticks()

        self.place.center = (screen_width / 2, screen_height / 2)

        if current_time - self.score_time < 700:
            number_three = Game_Font.render("3", False, Light_Grey)
            Screen.blit(
                number_three,
                (
                    screen_width / 2 - 10,
                    screen_height / 2 + 20,
                ),
            )

        if 700 < current_time - self.score_time < 1400:
            number_two = Game_Font.render("2", False, Light_Grey)
            Screen.blit(
                number_two,
                (
                    screen_width / 2 - 10,
                    screen_height / 2 + 20,
                ),
            )

        if 1400 < current_time - self.score_time < 2100:
            number_one = Game_Font.render("1", False, Light_Grey)
            Screen.blit(
                number_one,
                (
                    screen_width / 2 - 10,
                    screen_height / 2 + 20,
                ),
            )

        if current_time - self.score_time < 2100:
            self.speed_x, self.speed_y = 0, 0

        else:
            self.speed_x = 7 * random.choice((1, -1))
            self.speed_y = 7 * random.choice((1, -1))
            self.score_check = None


def event_pong(player, event):
    """.

    In this function we get the data from user

    """
    if event.type == pygame.QUIT:
        pygame.quit()
        sys.exit()

    if event.type == pygame.KEYDOWN:
        if event.key == pygame.K_DOWN:
            player.speed += 7

        if event.key == pygame.K_UP:
            player.speed -= 7

    if event.type == pygame.KEYUP:
        if event.key == pygame.K_DOWN:
            player.speed -= 7

        if event.key == pygame.K_UP:
            player.speed += 7


pygame.init()

clock = pygame.time.Clock()


# Create Enviroment
SCREEN_WIDTH = 1280
SCREEN_HEIGHT = 800
Screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Pong")

Background_Color = pygame.Color("gray12")
Light_Grey = (200, 200, 200)

ball_Speed_x = 7 * random.choice((1, -1))
ball_Speed_y = 7 * random.choice((1, -1))


Game_Font = pygame.font.Font("freesansbold.ttf", 32)
Pong_Sound = pygame.mixer.Sound(
    ".\\music\\Powerful-Trap.mp3",
)
Score_Sound = pygame.mixer.Sound(
    ".\\music\\goal.mp3",
)

pygame.mixer.Sound.play(Pong_Sound)


Player_Home = Player("player_home", "player", 0, "Home")
Cpu = Player("cpu", "cpu", 18, "guest")
ball = Ball("1", 15, 15)


while True:
    for action in pygame.event.get():
        event_pong(Player_Home, action)

        event_pong(Player_Home, action)

    ball.ball_animation(Player_Home, Cpu, SCREEN_WIDTH, SCREEN_HEIGHT)
    Player_Home.player_animation(SCREEN_HEIGHT)
    Cpu.opponent_cpu(SCREEN_HEIGHT, ball)

    Screen.fill(Background_Color)
    pygame.draw.rect(Screen, Light_Grey, Player_Home.placement)
    pygame.draw.rect(Screen, Light_Grey, Cpu.placement)
    pygame.draw.ellipse(Screen, Light_Grey, ball.place)
    pygame.draw.aaline(
        Screen,
        Light_Grey,
        (SCREEN_WIDTH / 2, 0),
        (SCREEN_WIDTH / 2, SCREEN_HEIGHT),
    )

    if ball.score_check:
        Ball.ball_restart(ball, SCREEN_WIDTH, SCREEN_HEIGHT)

    Player_Home.text = str(Player_Home.score)
    Screen.blit(
        Game_Font.render(Player_Home.text, True, Light_Grey),
        (660, 400),
    )

    Cpu.text = str(Cpu.score)
    Screen.blit(Game_Font.render(Cpu.text, True, Light_Grey), (600, 400))

    pygame.display.flip()
    clock.tick(60)
