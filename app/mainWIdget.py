from kivy import *
from kivy.uix.boxlayout import BoxLayout
from kivy.core.window import Window
import kivy
from kivy.app import App
from kivy.uix.label import Label


class MainWidget(BoxLayout):
    def __init__(self, **kwargs) -> None:
        super().__init__()
        Window.maximize()