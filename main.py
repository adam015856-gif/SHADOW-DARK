import json
import os

from kivy.app import App
from kivy.lang import Builder
from kivy.metrics import dp
from kivy.properties import ListProperty
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.popup import Popup
from kivy.utils import platform

KV = r"""
<ShadowButton@Button>:
    background_normal: ""
    background_color: (0.30, 0.08, 0.52, 1)
    color: (1, 1, 1, 1)
    size_hint_y: None
    height: dp(46)

BoxLayout:
    orientation: "vertical"
    padding: dp(16)
    spacing: dp(10)
    canvas.before:
        Color:
            rgba: (0.035, 0.035, 0.05, 1)
        Rectangle:
            pos: self.pos
            size: self.size

    Label:
        text: "[b]SHADOW DARK[/b]"
        markup: True
        font_size: "28sp"
        color: (0.75, 0.38, 1, 1)
        size_hint_y: None
        height: dp(55)

    Label:
        text: "PRIVATE GAME LAUNCHER"
        font_size: "11sp"
        color: (0.68, 0.68, 0.74, 1)
        size_hint_y: None
        height: dp(22)

    TextInput:
        id: package_input
        hint_text: "Package name (example: com.example.game)"
        multiline: False
        size_hint_y: None
        height: dp(48)
        background_color: (0.12, 0.12, 0.16, 1)
        foreground_color: (1, 1, 1, 1)
        cursor_color: (0.75, 0.38, 1, 1)
        padding: dp(10), dp(14)

    ShadowButton:
        text: "ADD GAME"
        on_release: app.add_game(package_input.text)

    Label:
        text: "MY GAMES"
        bold: True
        color: (0.75, 0.38, 1, 1)
        size_hint_y: None
        height: dp(28)

    ScrollView:
        do_scroll_x: False
        GridLayout:
            id: game_list
            cols: 1
            spacing: dp(8)
            size_hint_y: None
            height: self.minimum_height

    Label:
        text: "This app launches games from this list. It cannot hide apps from Samsung's system app drawer."
        color: (0.62, 0.62, 0.68, 1)
        font_size: "10sp"
        size_hint_y: None
        height: dp(42)
"""


class ShadowDarkApp(App):
    games = ListProperty([])

    def build(self):
        self.title = "SHADOW DARK"
        self.data_file = os.path.join(self.user_data_dir, "games.json")
        try:
            with open(self.data_file, "r", encoding="utf-8") as file:
                self.games = json.load(file)
        except (OSError, ValueError):
            self.games = []

        self.root_ui = Builder.load_string(KV)
        self.refresh_games()
        return self.root_ui

    def message(self, text):
        Popup(
            title="SHADOW DARK",
            content=Label(text=text),
            size_hint=(0.85, 0.30)
        ).open()

    def save_games(self):
        os.makedirs(self.user_data_dir, exist_ok=True)
        with open(self.data_file, "w", encoding="utf-8") as file:
            json.dump(self.games, file)

    def add_game(self, package_name):
        package_name = package_name.strip()
        if not package_name or "." not in package_name:
            self.message("Enter a valid Android package name.")
            return
        if package_name in self.games:
            self.message("This game is already in your list.")
            return

        self.games.append(package_name)
        self.save_games()
        self.refresh_games()
        self.root_ui.ids.package_input.text = ""

    def refresh_games(self):
        game_list = self.root_ui.ids.game_list
        game_list.clear_widgets()

        if not self.games:
            game_list.add_widget(Label(
                text="No games added yet.",
                color=(0.75, 0.75, 0.80, 1),
                size_hint_y=None,
                height=dp(48)
            ))

        for package_name in self.games:
            row = BoxLayout(
                orientation="horizontal",
                spacing=dp(6),
                size_hint_y=None,
                height=dp(46)
            )
            label = Label(
                text=package_name,
                color=(1, 1, 1, 1),
                halign="left",
                valign="middle"
            )
            label.bind(size=lambda widget, size: setattr(widget, "text_size", size))

            open_button = Button(
                text="OPEN",
                size_hint_x=None,
                width=dp(72),
                background_normal="",
                background_color=(0.12, 0.42, 0.25, 1)
            )
            open_button.bind(
                on_release=lambda _button, p=package_name: self.launch_game(p)
            )

            delete_button = Button(
                text="REMOVE",
                size_hint_x=None,
                width=dp(82),
                background_normal="",
                background_color=(0.42, 0.12, 0.16, 1)
            )
            delete_button.bind(
                on_release=lambda _button, p=package_name: self.remove_game(p)
            )

            row.add_widget(label)
            row.add_widget(open_button)
            row.add_widget(delete_button)
            game_list.add_widget(row)

    def launch_game(self, package_name):
        if platform != "android":
            self.message("Opening games is available in the Android APK.")
            return

        try:
            from jnius import autoclass
            PythonActivity = autoclass("org.kivy.android.PythonActivity")
            Intent = autoclass("android.content.Intent")

            activity = PythonActivity.mActivity
            package_manager = activity.getPackageManager()
            intent = package_manager.getLaunchIntentForPackage(package_name)

            if intent is None:
                self.message("Game not found. Check its package name.")
                return

            intent.addFlags(Intent.FLAG_ACTIVITY_NEW_TASK)
            activity.startActivity(intent)

        except Exception as error:
            self.message("Could not open game: " + str(error))

    def remove_game(self, package_name):
        self.games = [item for item in self.games if item != package_name]
        self.save_games()
        self.refresh_games()


if __name__ == "__main__":
    ShadowDarkApp().run()
