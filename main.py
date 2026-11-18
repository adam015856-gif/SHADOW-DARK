with open('main.py', 'w') as f:
    f.write('''# Python | main.py | Kivy | Android
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.slider import Slider
from kivy.core.window import Window

class ShadowFly(App):
    def build(self):
        Window.clearcolor = (0.025, 0.03, 0.04, 1)
        root = BoxLayout(orientation="vertical", padding=20, spacing=12)

        title = Label(text="[b]SHADOW FLY[/b]", markup=True, font_size=30, color=(0.2, 1, 0.35, 1), size_hint_y=None, height=70)
        root.add_widget(title)

        self.status = Label(text="STATUS: OFF", font_size=18)
        root.add_widget(self.status)

        fly = Button(text="FLY", background_color=(0.1, 0.8, 0.25, 1), size_hint_y=None, height=65)
        fly.bind(on_press=self.toggle_fly)
        root.add_widget(fly)

        root.add_widget(Label(text="FLIGHT SPEED"))
        self.speed = Slider(min=1, max=100, value=30)
        root.add_widget(self.speed)

        root.add_widget(Label(text="FLIGHT HEIGHT"))
        self.height = Slider(min=1, max=100, value=20)
        root.add_widget(self.height)

        stop = Button(text="STOP", background_color=(0.8, 0.1, 0.1, 1), size_hint_y=None, height=55)
        stop.bind(on_press=self.stop_fly)
        root.add_widget(stop)

        return root

    def toggle_fly(self, instance):
        self.status.text = "STATUS: FLY REQUESTED"

    def stop_fly(self, instance):
        self.status.text = "STATUS: OFF"

ShadowFly().run()
''')
