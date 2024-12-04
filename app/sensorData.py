import json
import serial
import threading
from time import sleep
from kivy.uix.boxlayout import BoxLayout
from kivy.clock import Clock
from kivy_garden.graph import LinePlot
import serial.serialutil
from random import randint #

class SensorData:
    def __init__(self, port, baudrate=9600):
        self.port = port
        self.baudrate = baudrate
        self.data = {"temperatura": 0, "pressão": 0, "empuxo": 0}
        try:
            self.serial = serial.Serial(self.port, self.baudrate)
            threading.Thread(target=self.read_serial_data, daemon=True).start()
        except serial.serialutil.SerialException:
            print(f"{self.port} inválida")

    def read_serial_data(self):
        while True:
            if self.serial.in_waiting > 0:
                try:
                    data = self.serial.readline().decode('utf-8').strip()
                    self.data = json.loads(data)
                except json.JSONDecodeError:
                    print("Erro ao decodificar o JSON.")
            sleep(1)

class MainWidget(BoxLayout):
    def __init__(self, sensor_data, **kwargs):
        super().__init__(**kwargs)
        self.sensor_data = sensor_data
    
        self.create_graph()
        Clock.schedule_interval(self.update_data, .1)

    def update_data(self, dt):
        # separa os dados vindos do serial
        data = self.sensor_data.data
        data = {"temperatura": (randint(0,100)), "pressão": randint(0,100), "empuxo": randint(0,100)} #
        self.temperatura = data.get("temperatura", 0)
        self.pressao = data.get("pressão", 0)
        self.empuxo = data.get("empuxo", 0)

        # atualiza as labels
        self.ids.temp.text = "Temperatura: " + str(self.temperatura)
        self.ids.pressao.text = "Pressão: " + str(self.pressao)
        self.ids.empuxo.text = "Empuxo: " + str(self.empuxo)

        self.update_graph()

    def update_graph(self):
        # atualiza lista com os valores do serial
        self.temp_points.append((self.temperatura, len(self.temp_points)))
        self.press_points.append((self.pressao, len(self.press_points)))
        self.empuxo_points.append((self.empuxo, len(self.empuxo_points)))
        
        # recolhe os últimos 100 pontos da lista
        self.temp_vpoints = self.temp_points[-100:]
        self.press_vpoints = self.press_points[-100:]
        self.empuxo_vpoints = self.empuxo_points[-100:]

        # atualiza os pontos visíveis no gráfico
        self.temp_plot.points = self.temp_vpoints
        self.press_plot.points = self.press_vpoints
        self.empuxo_plot.points = self.empuxo_vpoints
        
        # faz com que o gráfico seja dinâmico em y
        if(len(self.temp_points) > 100):
            self.ids.temp_graph.ymin = self.temp_vpoints[0][1]
            self.ids.temp_graph.ymax = self.temp_vpoints[-1][1]
            self.ids.press_graph.ymin = self.press_vpoints[0][1]
            self.ids.press_graph.ymax = self.press_vpoints[-1][1]
            self.ids.empuxo_graph.ymin = self.empuxo_vpoints[0][1]
            self.ids.empuxo_graph.ymax = self.empuxo_vpoints[-1][1]

    def create_graph(self):
        # atribui ao ID no .kv, cria o plot e a lista de pontos
        self.temp_graph = self.ids.temp_graph 
        self.temp_plot = LinePlot(line_width=1.5, color=[1, 0, 0, 1])
        self.ids.temp_graph.add_plot(self.temp_plot)
        self.temp_points = []

        self.press_graph = self.ids.press_graph
        self.press_plot = LinePlot(line_width=1.5, color=[0, 1, 0, 1])
        self.ids.press_graph.add_plot(self.press_plot)
        self.press_points = []

        self.empuxo_graph = self.ids.empuxo_graph
        self.empuxo_plot = LinePlot(line_width=1.5, color=[0, 0, 1, 1])
        self.ids.empuxo_graph.add_plot(self.empuxo_plot)
        self.empuxo_points = []