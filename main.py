# language: Python, file: main.py, runtime: Kivy 2.3+, target: Android (Buildozer)
# لعبة فضاء — تحكم باللمس، تجنّب الكويكبات، اجمع النجوم

from kivy.app import App
from kivy.uix.widget import Widget
from kivy.properties import NumericProperty, ReferenceListProperty, ObjectProperty
from kivy.vector import Vector
from kivy.clock import Clock
from kivy.core.window import Window
import random

Window.clearcolor = (0.02, 0.02, 0.08, 1)


class Ship(Widget):
    velocity_x = NumericProperty(0)
    velocity_y = NumericProperty(0)
    velocity = ReferenceListProperty(velocity_x, velocity_y)

    def move(self):
        self.pos = Vector(*self.velocity) + self.pos


class Asteroid(Widget):
    velocity_x = NumericProperty(0)
    velocity_y = NumericProperty(0)
    velocity = ReferenceListProperty(velocity_x, velocity_y)

    def move(self):
        self.pos = Vector(*self.velocity) + self.pos


class Star(Widget):
    pass


class Game(Widget):
    ship = ObjectProperty(None)
    score = NumericProperty(0)
    lives = NumericProperty(3)

    def __init__(self, **kw):
        super().__init__(**kw)
        self.asteroids = []
        self.stars = []
        self.target = None

    def start(self):
        self.ship.center = self.center_x, 120
        self.score = 0
        self.lives = 3
        self.asteroids = []
        self.stars = []
        Clock.unschedule(self.spawn_asteroid)
        Clock.unschedule(self.spawn_star)
        Clock.unschedule(self.update)
        Clock.schedule_interval(self.spawn_asteroid, 1.2)
        Clock.schedule_interval(self.spawn_star, 0.8)
        Clock.schedule_interval(self.update, 1 / 60)

    def spawn_asteroid(self, dt):
        a = Asteroid(size=(random.randint(35, 60),) * 2,
                     pos=(random.randint(0, int(self.width - 60)), self.height))
        a.velocity = (random.uniform(-40, 40), random.uniform(-320, -180))
        self.asteroids.append(a)
        self.add_widget(a)

    def spawn_star(self, dt):
        s = Star(size=(24, 24),
                 pos=(random.randint(0, int(self.width - 24)), self.height))
        self.stars.append(s)
        self.add_widget(s)

    def on_touch_move(self, touch):
        if self.ship:
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
                if self.lives <= 0:
                    self.game_over()

        for s in self.stars[:]:
            s.y -= 220 * dt
            if s.top < 0:
                self.remove_widget(s)
                self.stars.remove(s)
            elif self.ship.collide_widget(s):
                self.remove_widget(s)
                self.stars.remove(s)
                self.score += 10

    def game_over(self):
        Clock.unschedule(self.update)
        Clock.unschedule(self.spawn_asteroid)
        Clock.unschedule(self.spawn_star)
        self.ship.center = self.center_x, self.center_y


class GameApp(App):
    def build(self):
        game = Game()
        game.start()
        return game


if __name__ == "__main__":
    GameApp().run()
