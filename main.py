import json
import os
from kivy.app import App
from kivy.core.window import Window
from kivy.graphics import Color, Rectangle
from kivy.metrics import dp
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.popup import Popup
from kivy.uix.scrollview import ScrollView
from kivy.uix.textinput import TextInput
from kivy.utils import platform

Window.clearcolor = (0.06, 0.06, 0.09, 1)

VAULT_FILE = "shadow_dark_vault.json"


class DarkCard(BoxLayout):
    def __init__(self, bg_color=(0.11, 0.11, 0.16, 1), **kwargs):
        super().__init__(**kwargs)
        with self.canvas.before:
            self._bg_color = Color(*bg_color)
            self._rect = Rectangle(pos=self.pos, size=self.size)
        self.bind(pos=self._update_rect, size=self._update_rect)

    def _update_rect(self, *args):
        self._rect.pos = self.pos
        self._rect.size = self.size


class ShadowDarkApp(App):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.pin_code = "1234"
        self.hidden_packages = set()
        self.unlocked = False
        self.current_tab = "visible"

    def build(self):
        self.title = "SHADOW DARK"
        self._load_state()

        root = BoxLayout(orientation="vertical", padding=dp(12), spacing=dp(10))

        # Top header
        header = DarkCard(
            orientation="horizontal",
            size_hint_y=None,
            height=dp(56),
            padding=[dp(14), dp(8)],
            spacing=dp(10),
        )
        title_lbl = Label(
            text="SHADOW DARK",
            font_size="20sp",
            bold=True,
            color=(0.85, 0.25, 1.0, 1),
            halign="left",
            valign="middle",
        )
        title_lbl.bind(size=title_lbl.setter("text_size"))

        self.lock_btn = Button(
            text="Unlock Vault",
            size_hint_x=None,
            width=dp(120),
            background_normal="",
            background_color=(0.25, 0.12, 0.35, 1),
            color=(1, 1, 1, 1),
        )
        self.lock_btn.bind(on_release=self._toggle_vault_lock)

        header.add_widget(title_lbl)
        header.add_widget(self.lock_btn)
        root.add_widget(header)

        # Tabs
        tabs = BoxLayout(size_hint_y=None, height=dp(44), spacing=dp(8))
        self.btn_visible = Button(
            text="Games List",
            background_normal="",
            background_color=(0.45, 0.15, 0.75, 1),
        )
        self.btn_hidden = Button(
            text="Hidden Vault",
            background_normal="",
            background_color=(0.16, 0.16, 0.22, 1),
        )
        self.btn_set_pin = Button(
            text="Set PIN",
            size_hint_x=None,
            width=dp(90),
            background_normal="",
            background_color=(0.18, 0.18, 0.25, 1),
        )

        self.btn_visible.bind(on_release=lambda *_: self._switch_tab("visible"))
        self.btn_hidden.bind(on_release=lambda *_: self._switch_tab("hidden"))
        self.btn_set_pin.bind(on_release=self._open_set_pin_popup)

        tabs.add_widget(self.btn_visible)
        tabs.add_widget(self.btn_hidden)
        tabs.add_widget(self.btn_set_pin)
        root.add_widget(tabs)

        # Status bar
        self.status_lbl = Label(
            text="",
            size_hint_y=None,
            height=dp(26),
            font_size="13sp",
            color=(0.75, 0.75, 0.85, 1),
        )
        root.add_widget(self.status_lbl)

        # Scrollable list
        scroll = ScrollView(do_scroll_x=False)
        self.list_container = BoxLayout(
            orientation="vertical",
            size_hint_y=None,
            spacing=dp(8),
            padding=[0, dp(4), 0, dp(12)],
        )
        self.list_container.bind(minimum_height=self.list_container.setter("height"))
        scroll.add_widget(self.list_container)
        root.add_widget(scroll)

        self.refresh_list()
        return root

    def _storage_path(self):
        base = self.user_data_dir if self.user_data_dir else "."
        os.makedirs(base, exist_ok=True)
        return os.path.join(base, VAULT_FILE)

    def _load_state(self):
        path = self._storage_path()
        if os.path.exists(path):
            try:
                with open(path, "r", encoding="utf-8") as f:
                    data = json.load(f)
                self.pin_code = str(data.get("pin", "1234"))
                self.hidden_packages = set(data.get("hidden", []))
            except Exception:
                pass

    def _save_state(self):
        path = self._storage_path()
        try:
            with open(path, "w", encoding="utf-8") as f:
                json.dump(
                    {
                        "pin": self.pin_code,
                        "hidden": sorted(self.hidden_packages),
                    },
                    f,
                    indent=2,
                )
        except Exception:
            pass

    def _get_installed_apps(self):
        if platform == "android":
            try:
                from jnius import autoclass

                PythonActivity = autoclass("org.kivy.android.PythonActivity")
                Intent = autoclass("android.content.Intent")
                PackageManager = autoclass("android.content.pm.PackageManager")

                activity = PythonActivity.mActivity
                pm = activity.getPackageManager()

                main_intent = Intent(Intent.ACTION_MAIN, None)
                main_intent.addCategory(Intent.CATEGORY_LAUNCHER)

                resolve_infos = pm.queryIntentActivities(main_intent, 0)
                apps = []
                seen = set()

                for i in range(resolve_infos.size()):
                    ri = resolve_infos.get(i)
                    pkg = ri.activityInfo.packageName
                    if pkg == activity.getPackageName() or pkg in seen:
                        continue
                    seen.add(pkg)
                    label = ri.loadLabel(pm).toString()
                    apps.append({"name": label, "package": pkg})

                apps.sort(key=lambda item: item["name"].lower())
                return apps
            except Exception as e:
                self.status_lbl.text = f"Error reading apps: {e}"
                return []
        else:
            # Sample data for desktop testing
            return [
                {"name": "Shadow Strike Arena", "package": "com.shadow.strike"},
                {"name": "Dark Rift Legends", "package": "com.dark.rift"},
                {"name": "Neon Drift Rush", "package": "com.neon.drift"},
                {"name": "Void Survival 3D", "package": "com.void.survival"},
            ]

    def _launch_package(self, package_name):
        if platform == "android":
            try:
                from jnius import autoclass

                PythonActivity = autoclass("org.kivy.android.PythonActivity")
                activity = PythonActivity.mActivity
                pm = activity.getPackageManager()
                launch_intent = pm.getLaunchIntentForPackage(package_name)
                if launch_intent:
                    activity.startActivity(launch_intent)
                else:
                    self.status_lbl.text = "Cannot launch package."
            except Exception as e:
                self.status_lbl.text = f"Launch error: {e}"
        else:
            self.status_lbl.text = f"Simulated launch: {package_name}"

    def _toggle_vault_lock(self, *_):
        if self.unlocked:
            self.unlocked = False
            self.lock_btn.text = "Unlock Vault"
            if self.current_tab == "hidden":
                self._switch_tab("visible")
            else:
                self.refresh_list()
        else:
            self._open_pin_popup(on_success=self._on_vault_unlocked)

    def _on_vault_unlocked(self):
        self.unlocked = True
        self.lock_btn.text = "Lock Vault"
        self.refresh_list()

    def _switch_tab(self, tab_name):
        if tab_name == "hidden" and not self.unlocked:
            self._open_pin_popup(
                on_success=lambda: self._complete_tab_switch("hidden")
            )
            return
        self._complete_tab_switch(tab_name)

    def _complete_tab_switch(self, tab_name):
        self.unlocked = True if tab_name == "hidden" else self.unlocked
        if self.unlocked:
            self.lock_btn.text = "Lock Vault"
        self.current_tab = tab_name
        self.btn_visible.background_color = (
            (0.45, 0.15, 0.75, 1) if tab_name == "visible" else (0.16, 0.16, 0.22, 1)
        )
        self.btn_hidden.background_color = (
            (0.45, 0.15, 0.75, 1) if tab_name == "hidden" else (0.16, 0.16, 0.22, 1)
        )
        self.refresh_list()

    def _toggle_hide_package(self, package_name):
        if package_name in self.hidden_packages:
            self.hidden_packages.remove(package_name)
        else:
            self.hidden_packages.add(package_name)
        self._save_state()
        self.refresh_list()

    def _open_pin_popup(self, on_success):
        box = BoxLayout(orientation="vertical", padding=dp(12), spacing=dp(10))
        inp = TextInput(
            hint_text="Enter PIN",
            password=True,
            multiline=False,
            input_filter="int",
            size_hint_y=None,
            height=dp(44),
        )
        msg = Label(text="", size_hint_y=None, height=dp(24), color=(1, 0.35, 0.35, 1))
        btn_row = BoxLayout(size_hint_y=None, height=dp(42), spacing=dp(8))
        btn_ok = Button(text="Confirm", background_normal="", background_color=(0.45, 0.15, 0.75, 1))
        btn_cancel = Button(text="Cancel", background_normal="", background_color=(0.25, 0.25, 0.3, 1))

        popup = Popup(
            title="SHADOW DARK PIN",
            content=box,
            size_hint=(0.85, None),
            height=dp(220),
            auto_dismiss=False,
        )

        def check_pin(*_):
            if inp.text.strip() == self.pin_code:
                popup.dismiss()
                on_success()
            else:
                msg.text = "Wrong PIN"

        btn_ok.bind(on_release=check_pin)
        btn_cancel.bind(on_release=lambda *_: popup.dismiss())
        box.add_widget(inp)
        box.add_widget(msg)
        btn_row.add_widget(btn_ok)
        btn_row.add_widget(btn_cancel)
        box.add_widget(btn_row)
        popup.open()

    def _open_set_pin_popup(self, *_):
        box = BoxLayout(orientation="vertical", padding=dp(12), spacing=dp(10))
        inp = TextInput(
            hint_text="New 4+ digit PIN",
            password=True,
            multiline=False,
            input_filter="int",
            size_hint_y=None,
            height=dp(44),
        )
        btn_save = Button(
            text="Save PIN",
            size_hint_y=None,
            height=dp(42),
            background_normal="",
            background_color=(0.45, 0.15, 0.75, 1),
        )
        popup = Popup(
            title="Set Vault PIN",
            content=box,
            size_hint=(0.85, None),
            height=dp(190),
        )

        def save_new_pin(*_):
            val = inp.text.strip()
            if len(val) >= 4:
                self.pin_code = val
                self._save_state()
                self.status_lbl.text = "PIN updated successfully."
                popup.dismiss()
            else:
                self.status_lbl.text = "PIN must be at least 4 digits."

        btn_save.bind(on_release=save_new_pin)
        box.add_widget(inp)
        box.add_widget(btn_save)
        popup.open()

    def refresh_list(self):
        self.list_container.clear_widgets()
        all_apps = self._get_installed_apps()

        if self.current_tab == "visible":
            items = [a for a in all_apps if a["package"] not in self.hidden_packages]
            self.status_lbl.text = (
                f"Shown: {len(items)} | Hidden in Vault: {len(self.hidden_packages)}"
            )
        else:
            if not self.unlocked:
                self.status_lbl.text = "Vault is locked."
                return
            items = [a for a in all_apps if a["package"] in self.hidden_packages]
            self.status_lbl.text = f"Hidden Vault items: {len(items)}"

        if not items:
            empty_lbl = Label(
                text="No items to display here.",
                size_hint_y=None,
                height=dp(60),
                color=(0.65, 0.65, 0.75, 1),
            )
            self.list_container.add_widget(empty_lbl)
            return

        for app in items:
            pkg = app["package"]
            name = app["name"]
            is_hidden = pkg in self.hidden_packages

            card = DarkCard(
                orientation="horizontal",
                size_hint_y=None,
                height=dp(64),
                padding=[dp(10), dp(8)],
                spacing=dp(8),
            )

            info_box = BoxLayout(orientation="vertical")
            lbl_name = Label(
                text=name,
                font_size="15sp",
                bold=True,
                halign="left",
                valign="middle",
                color=(1, 1, 1, 1),
            )
            lbl_name.bind(size=lbl_name.setter("text_size"))

            lbl_pkg = Label(
                text=pkg,
                font_size="11sp",
                halign="left",
                valign="middle",
                color=(0.6, 0.6, 0.72, 1),
            )
            lbl_pkg.bind(size=lbl_pkg.setter("text_size"))

            info_box.add_widget(lbl_name)
            info_box.add_widget(lbl_pkg)

            btn_open = Button(
                text="Open",
                size_hint_x=None,
                width=dp(68),
                background_normal="",
                background_color=(0.15, 0.55, 0.35, 1),
            )
            btn_open.bind(on_release=lambda _, p=pkg: self._launch_package(p))

            btn_action = Button(
                text="Unhide" if is_hidden else "Hide",
                size_hint_x=None,
                width=dp(76),
                background_normal="",
                background_color=(0.65, 0.2, 0.25, 1) if not is_hidden else (0.35, 0.2, 0.65, 1),
            )
            btn_action.bind(on_release=lambda _, p=pkg: self._toggle_hide_package(p))

            card.add_widget(info_box)
            card.add_widget(btn_open)
            card.add_widget(btn_action)
            self.list_container.add_widget(card)


if __name__ == "__main__":
    ShadowDarkApp().run()
