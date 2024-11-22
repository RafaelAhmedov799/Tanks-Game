import math

import arcade

SCREEN_WIDTH = 960
SCREEN_HEIGHT = 720
R = 100

class Window(arcade.Window):
    def __init__(self, WIDTH, HEIGHT,title):
        super().__init__(WIDTH, HEIGHT, title)
        self.angle=0
        self.symbol=""

    def on_draw(self):
        self.clear((0,0,0))
        arcade.draw_arc_outline(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2, 2 * R, 2 * R, arcade.color.WHITE, start_angle=0, end_angle=360, border_width=3)
        arcade.draw_arc_outline(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2, 2, 2, arcade.color.WHITE, start_angle=0, end_angle=360, border_width=3)
        arcade.draw_arc_outline(math.cos(math.radians(self.angle)) * R + SCREEN_WIDTH / 2, math.sin(math.radians(self.angle)) * R + SCREEN_HEIGHT / 2, 2, 2, arcade.color.YELLOW, start_angle=0, end_angle=360, border_width=3)
        arcade.draw_text(f"{self.angle}", SCREEN_WIDTH - 10, 0 + 10, anchor_x="right", font_size=20)
        arcade.draw_text(f"{round(math.cos(math.radians(self.angle)),1)}", SCREEN_WIDTH - 10 - 80, 0 + 10, anchor_x="right", font_size=20, color=arcade.color.GREEN)
        arcade.draw_text(f"{round(math.sin(math.radians(self.angle)),1)}", SCREEN_WIDTH - 10 - 140, 0 + 10, anchor_x="right", font_size=20, color=arcade.color.RED)
        arcade.draw_line(0 + SCREEN_WIDTH / 2, 0 + SCREEN_HEIGHT / 2, math.cos(math.radians(self.angle)) * R + SCREEN_WIDTH / 2,
                         math.sin(math.radians(self.angle)) * R + SCREEN_HEIGHT / 2, arcade.color.WHITE, 2)
        arcade.draw_line(0 + SCREEN_WIDTH / 2, 0 + SCREEN_HEIGHT / 2, math.cos(math.radians(self.angle)) * R + SCREEN_WIDTH / 2,
                         0 + SCREEN_HEIGHT / 2, arcade.color.GREEN, 2)
        arcade.draw_line(0 + SCREEN_WIDTH / 2, 0 + SCREEN_HEIGHT / 2, 0 + SCREEN_WIDTH / 2,
                         math.sin(math.radians(self.angle)) * R + SCREEN_HEIGHT / 2, arcade.color.RED, 2)

    def update(self, delta_time: float):
        if self.symbol == arcade.key.A:
            self.angle += 1
        if self.symbol == arcade.key.D:
            self.angle -= 1
    def on_key_press(self, symbol: int, modifiers: int):
        self.symbol=symbol
    def on_key_release(self, symbol: int, modifiers: int):
        self.symbol=""
window = Window(SCREEN_WIDTH, SCREEN_HEIGHT, "TANK")
arcade.run()
