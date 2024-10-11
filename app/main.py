from kivy.app import App
from mainWIdget import MainWidget
from kivy.lang.builder import Builder

class MainApp(App):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def build(self):
        self.widget = MainWidget()
        return self.widget


if __name__ == '__main__':
    Builder.load_string(open(r'app\mainWidget.kv', encoding='utf8').read(), rulesonly=True)
    MainApp().run()
    MainApp().stop()
