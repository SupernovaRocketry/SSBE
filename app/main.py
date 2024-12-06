from kivy.app import App
from kivy.lang.builder import Builder
from sensorData import *

class MainApp(App):
    def build(self):
        sensor_data = SensorData(port='COM4', baudrate=9600)
        return MainWidget(sensor_data)

    def on_image_click(self):
        print("Imagem clicada")

if __name__ == '__main__':
    Builder.load_string(open('sensorData.kv', encoding='utf8').read(), rulesonly=True)
    MainApp().run()
    MainApp().stop()
