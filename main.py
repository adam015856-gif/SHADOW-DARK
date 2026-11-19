from kivy.app import App
from kivy.uix.widget import Widget
from kivy.uix.label import Label
from kivy.properties import NumericProperty, ListProperty
from kivy.vector import Vector
from kivy.clock import Clock
from kivy.core.window import Window
from kivy.graphics import Color, Ellipse, Rectangle, Triangle
import random

Window.clearcolor = (0.02, 0.02, 0.08, 1)


class Ship(Widget):
    velocity = ListProperty([0, 0])

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        with self.canvas:
            Color(0.2, 0.8, 1, 1)
            self.body = Triangle(points=[
                self.center_x, self.top,
                self.x, self.y,
                self.right, self.y
            ])
        self.bind(pos=self.update_shape, size=self.update_shape)

    def update_shape(self, *args):
        self.body.points = [
            self.center_x, self.top,
            self.x, self.y,
            self.right, self.y
        ]

    def move(self):
        self.pos = Vector(*self.velocity) + self.pos


class Asteroid(Widget):
    velocity = ListProperty([0, 0])

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        with self.canvas:
            Color(0.65, 0.4, 0.25, 1)
            self.shape = Ellipse(pos=self.pos, size=self.size)
        self.bind(pos=self.update_shape, size=self.update_shape)

    def update_shape(self, *args):
        self.shape.pos = self.pos
        self.shape.size = self.size

    def move(self):
        self.pos = Vector(*self.velocity) + self.pos


class Star(Widget):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        with self.canvas:
            Color(1, 0.85, 0.1, 1)
            self.shape = Ellipse(pos=self.pos, size=self.size)
        self.bind(pos=self.update_shape, size=self.update_shape)

    def update_shape(self, *args):
        self.shape.pos = self.pos
        self.shape.size = self.size


class Game(Widget):
    score = NumericProperty(0)
    lives = NumericProperty(3)

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.asteroids = []
        self.stars = []
        self.ship = Ship(size=(50, 50))
        self.add_widget(self.ship)

        self.hud = Label(
            text="Score: 0 | Lives: 3",
            pos=(15, Window.height - 50),
            size_hint=(None, None),
            size=(260, 40),
            color=(1, 1, 1, 1)
        )
        self.add_widget(self.hud)
        Window.bind(size=self.on_window_resize)

    def on_window_resize(self, instance, value):
        self.hud.pos = (15, self.height - 50)

    def start(self):
        for a in self.asteroids:
            self.remove_widget(a)
        for s in self.stars:
            self.remove_widget(s)
        self.asteroids.clear()
        self.stars.clear()

        self.score = 0
        self.lives = 3
        self.update_hud()
        self.ship.center = (self.width / 2, 120)

        Clock.unschedule(self.spawn_asteroid)
        Clock.unschedule(self.spawn_star)
        Clock.unschedule(self.update)
        Clock.schedule_interval(self.spawn_asteroid, 1.2)
        Clock.schedule_interval(self.spawn_star, 0.8)
        Clock.schedule_interval(self.update, 1 / 60)

    def update_hud(self):
        self.hud.text = f"Score: {self.score} | Lives: {self.lives}"

    def spawn_asteroid(self, dt):
        size_val = random.randint(36, 60)
        max_x = max(0, int(self.width - size_val))
        a = Asteroid(
            size=(size_val, size_val),
            pos=(random.randint(0, max_x), self.height)
        )
        a.velocity = [random.uniform(-40, 40), random.uniform(-320, -180)]
        self.asteroids.append(a)
        self.add_widget(a)

    def spawn_star(self, dt):
        max_x = max(0, int(self.width - 24))
        s = Star(
            size=(24, 24),
            pos=(random.randint(0, max_x), self.height)
        )
        self.stars.append(s)
        self.add_widget(s)

    def on_touch_move(self, touch):
        if self.ship and self.lives > 0:
            self.ship.center_x = max(30, min(self.width - 30, touch.x))
            self.ship.center_y = max(80, min(self.height - 30, touch.y))

    def update(self, dt):
        for a in self.asteroids[:]:
            a.move()
            if a.top < 0:
                self.remove_widget(a)
                self.asteroids.remove(a)
            elif self.ship.collide_widget(a):
                self.remove_widget(a)
                self.asteroids.remove(a)
                self.lives -= 1
                self.update_hud()
                if self.lives <= 0:
                    self.game_over()
                    return

        for s in self.stars[:]:
            s.y -= 220 * dt
            if s.top < 0:
                self.remove_widget(s)
                self.stars.remove(s)
            elif self.ship.collide_widget(s):
                self.remove_widget(s)
                self.stars.remove(s)
                self.score += 10
                self.update_hud()

    def game_over(self):
        Clock.unschedule(self.update)
        Clock.unschedule(self.spawn_asteroid)
        Clock.unschedule(self.spawn_star)
        self.hud.text = f"Game Over! Score: {self.score} (Tap to restart)"

    def on_touch_down(self, touch):
        if self.lives <= 0:
            self.start()
            return True
        return super().on_touch_down(touch)


class GameApp(App):
    def build(self):
        game = Game()
        Clock.schedule_once(lambda dt: game.start(), 0)
        return game


if __name__ == "__main__":
    GameApp().run()
