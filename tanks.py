import math
import sys
import time

import arcade

SCREEN_WIDTH = 960
SCREEN_HEIGHT = 720
SCREEN_TITLE = "Tanks"


class Game(arcade.Window):
    def __init__(self, width, height, title):
        super().__init__(width, height, title)
        self.background = arcade.load_texture("background.png")
        self.tank = GreenTank(350, SCREEN_HEIGHT / 2)
        self.bullets = arcade.SpriteList()
        self.red_tanks = arcade.SpriteList()
        self.red_base = RedBase(SCREEN_WIDTH / 1.5 + 150, SCREEN_HEIGHT / 2)
        self.green_base = GreenBase(SCREEN_WIDTH / 4 - 100, SCREEN_HEIGHT / 2)
        self.game = True

    def setup(self):
        for i in range(3):
            self.red_tanks.append(RedTank(SCREEN_WIDTH/1.6, SCREEN_HEIGHT/2-80+i*80))

    def on_draw(self):
        self.clear()
        arcade.draw_texture_rectangle(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2, SCREEN_WIDTH, SCREEN_HEIGHT, self.background)
        self.tank.draw()
        self.bullets.draw()
        for t in self.red_tanks:
            t.draw()
        self.red_base.draw()
        self.green_base.draw()
        if self.red_base.health <= 0:
            arcade.draw_text("You Won!", SCREEN_WIDTH / 2, SCREEN_HEIGHT - 50, arcade.color.YELLOW, 100,
                             anchor_x="center", anchor_y="top")
        elif not self.game:
            arcade.draw_text("You Lose", SCREEN_WIDTH / 2, SCREEN_HEIGHT - 50, arcade.color.YELLOW, 100,
                             anchor_x="center", anchor_y="top")

    def update(self, delta_time):
        if self.game:
            self.tank.update()
            self.bullets.update()
            self.red_tanks.update()
            for sprite in [self.red_base, self.green_base, self.tank] + list(self.red_tanks):
                bullets = arcade.check_for_collision_with_list(sprite, self.bullets)
                if len(bullets) > 0:
                    sprite.health -= 10
                for b in bullets:
                    b.kill()
            self.red_base.update()
            self.green_base.update()
            self.tank.update()
            self.red_tanks.update()
            if self.green_base.health <= 0 or self.tank.health <= 0:
                self.game = False


    def on_key_press(self, symbol: int, modifiers: int):
        if symbol == arcade.key.A:
            self.tank.change_angle = 1.5
        if symbol == arcade.key.D:
            self.tank.change_angle = -1.5
        if symbol == arcade.key.W:
            self.tank.speed = 2
        if symbol == arcade.key.S:
            self.tank.speed = -2
        if symbol == arcade.key.SPACE:
            self.tank.shoot()

    def on_key_release(self, symbol: int, modifiers: int):
        if symbol == arcade.key.A or symbol == arcade.key.D:
            self.tank.change_angle = 0
        if symbol == arcade.key.W or symbol == arcade.key.S:
            self.tank.speed = 0


class Tank(arcade.Sprite):
    def __init__(self, filename, center_x, center_y):
        super().__init__(filename, 0.15, center_x=center_x, center_y=center_y)
        self.speed = 0

    def update(self):
        super().update()
        self.change_x = math.cos(math.radians(self.angle))*self.speed
        self.change_y = math.sin(math.radians(self.angle))*self.speed

    def shoot(self, bullet_class):
        window.bullets.append(bullet_class(self.center_x + math.cos(math.radians(self.angle))*60,
                                           self.center_y + math.sin(math.radians(self.angle))*60, self.angle))


HBT_WIDTH = 125
HBT_MARGIN = 140
HBT_HEIGHT = 15


class GreenTank(Tank):
    def __init__(self, center_x, center_y):
        super().__init__("green.png", center_x, center_y)
        self.health = 100

    def shoot(self):
        super().shoot(GreenBullet)

    def draw(self, *, filter=None, pixelated=None, blend_function=None):
        super().draw()
        arcade.draw_rectangle_filled(self.center_x, self.center_y + HBT_MARGIN-100, HBT_WIDTH, HBT_HEIGHT, arcade.color.BLACK)
        arcade.draw_rectangle_filled(self.center_x - (100-self.health)/100 / 2 * HBT_WIDTH, self.center_y + HBT_MARGIN-100, HBT_WIDTH * self.health/100,
                                     HBT_HEIGHT, arcade.color.GREEN)


class Bullet(arcade.Sprite):
    def __init__(self, filename, center_x, center_y, angle):
        super().__init__(filename, 0.1, center_x=center_x, center_y=center_y)
        self.angle = angle
        self.change_x = math.cos(math.radians(self.angle)) * 10
        self.change_y = math.sin(math.radians(self.angle)) * 10


class GreenBullet(Bullet):
    def __init__(self, center_x, center_y, angle):
        super().__init__("green_bullet.png", center_x, center_y, angle)


class RedBullet(Bullet):
    def __init__(self, center_x, center_y, angle):
        super().__init__("red_bullet.png", center_x, center_y, angle)


class RedTank(Tank):
    def __init__(self, center_x, center_y):
        super().__init__("red.png", center_x, center_y)
        self.window = window
        self.health = 100
        self.last_shoot_time = time.time()
        self.speed = 1

    def shoot(self):
        super().shoot(RedBullet)

    def draw(self, *, filter=None, pixelated=None, blend_function=None):
        super().draw()
        arcade.draw_rectangle_filled(self.center_x, self.center_y + HBT_MARGIN-100, HBT_WIDTH, HBT_HEIGHT, arcade.color.WHITE)
        arcade.draw_rectangle_filled(self.center_x - (100 - self.health)/100 / 2 * HBT_WIDTH, self.center_y + HBT_MARGIN-100,
                                     HBT_WIDTH * self.health/100, HBT_HEIGHT, arcade.color.RED)

    def update(self):
        super().update()
        if time.time() - self.last_shoot_time > 2:
            self.shoot()
            self.last_shoot_time = time.time()
        distance_to_tank = arcade.get_distance_between_sprites(self, window.tank)
        distance_to_base = arcade.get_distance_between_sprites(self, window.green_base)
        if distance_to_base < distance_to_tank:
            target = window.green_base
            distance_to_target = distance_to_base
            if distance_to_target <= 160:
                self.change_x = 0
                self.change_y = 0
        else:
            target = window.tank
            distance_to_target = distance_to_tank
            if distance_to_target <= 80:
                self.change_x = 0
                self.change_y = 0
        if self.health <= 0:
            self.kill()
        dx = target.center_x - self.center_x
        dy = target.center_y - self.center_y
        self.angle = math.degrees(math.atan2(dy, dx))


HB_WIDTH = 250
HB_MARGIN = 175
HB_HEIGHT = 20


class RedBase(arcade.Sprite):
    def __init__(self, center_x, center_y):
        super().__init__("red_base.png", 1.5, center_x=center_x, center_y=center_y)
        self.health = 100

    def draw(self, *, filter=None, pixelated=None, blend_function=None):
        super().draw()
        arcade.draw_rectangle_filled(self.center_x, self.center_y + HB_MARGIN, HB_WIDTH, HB_HEIGHT, arcade.color.WHITE)
        arcade.draw_rectangle_filled(self.center_x - (100 - self.health)/100 / 2 * HB_WIDTH, self.center_y + HB_MARGIN,
                                     HB_WIDTH * self.health/100, HB_HEIGHT, arcade.color.RED)

    def update(self):
        if self.health <= sys.float_info.epsilon:
            window.game = False
            self.color = arcade.color.BLACK


class GreenBase(arcade.Sprite):
    def __init__(self, center_x, center_y):
        super().__init__("green_base.png", 1.3, center_x=center_x, center_y=center_y)
        self.health = 100

    def draw(self, *, filter=None, pixelated=None, blend_function=None):
        super().draw()
        arcade.draw_rectangle_filled(self.center_x, self.center_y + HB_MARGIN, HB_WIDTH, HB_HEIGHT, arcade.color.BLACK)
        arcade.draw_rectangle_filled(self.center_x - ((100-self.health)/100) / 2 * HB_WIDTH, self.center_y + HB_MARGIN, HB_WIDTH * self.health/100,
                                     HB_HEIGHT, arcade.color.GREEN)

    def update(self):
        if self.health <= sys.float_info.epsilon:
            window.game = False
            self.color = arcade.color.BLACK


window = Game(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)
window.setup()
arcade.run()
