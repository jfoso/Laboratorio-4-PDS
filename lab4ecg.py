import sys
from PyQt6.QtWidgets import (QMainWindow, QApplication, QPushButton, QVBoxLayout, QWidget, QFileDialog)
import numpy as np
import threading
import pandas as pd
import nidaqmx  # Librería para comunicarse con DAQ de National Instruments
from nidaqmx.constants import AcquisitionType
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
from datetime import datetime

class Principal(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Adquisición de Señal EMG")
        self.setGeometry(100, 100, 800, 600)
        
        # Crear layout principal
        self.layout = QVBoxLayout()
        self.container = QWidget()
        self.container.setLayout(self.layout)
        self.setCentralWidget(self.container)

        # Botones
        self.connect_btn = QPushButton("CONECTAR")
        self.save_btn = QPushButton("GUARDAR DATOS")
        self.show_btn = QPushButton("MOSTRAR INFORMACIÓN")

        # Agregar botones al layout
        self.layout.addWidget(self.connect_btn)
        self.layout.addWidget(self.save_btn)
        self.layout.addWidget(self.show_btn)

        # Inicializar gráfico
        self.fig = Figure()
        self.ax = self.fig.add_subplot(111)
        self.canvas = FigureCanvas(self.fig)
        self.layout.addWidget(self.canvas)
        
        # Variables de adquisición
        self.daq_task = None
        self.sampling_rate = 1000  # Frecuencia de muestreo (Hz)
        self.channel = "Dev4/ai0"  # Canal analógico del DAQ

        # Conectar botones
        self.connect_btn.clicked.connect(self.conectar_daq)
        self.save_btn.clicked.connect(self.guardar_datos)
        self.show_btn.clicked.connect(self.mostrar_informacion)

        # Datos para graficar
        self.x = np.linspace(0, 100, self.sampling_rate)  # 5 segundos de ventana
        self.y = np.zeros(len(self.x))

    def conectar_daq(self):
        """Inicia la adquisición desde el DAQ."""
        if self.daq_task is None:
            try:
                self.daq_task = nidaqmx.Task()
                self.daq_task.ai_channels.add_ai_voltage_chan(self.channel)
                self.daq_task.timing.cfg_samp_clk_timing(self.sampling_rate, sample_mode=AcquisitionType.CONTINUOUS)
                
                self.stop_event = threading.Event()
                self.hilo_daq = threading.Thread(target=self.recibir_datos)
                self.hilo_daq.start()
                
                self.connect_btn.setText("DESCONECTAR")
                print("DAQ conectado y adquiriendo datos...")
            except Exception as e:
                print("Error al conectar con DAQ:", e)
        else:
            self.desconectar_daq()

    def desconectar_daq(self):
        """Detiene la adquisición y desconecta el DAQ."""
        if self.daq_task is not None:
            self.stop_event.set()
            self.hilo_daq.join()
            self.daq_task.close()
            self.daq_task = None
            self.connect_btn.setText("CONECTAR")
            print("DAQ desconectado.")

    def recibir_datos(self):
        """Lee datos continuamente desde el DAQ y actualiza la gráfica."""
        while not self.stop_event.is_set():
            try:
                data = self.daq_task.read(number_of_samples_per_channel=10)  # Lee 10 muestras por ciclo
                for value in data:
                    self.y = np.roll(self.y, -1)
                    self.y[-1] = value  # Actualizar con nueva lectura

                self.ax.clear()
                self.ax.plot(self.x, self.y, label="EMG Señal")
                self.ax.grid(True)
                self.ax.legend()
                self.canvas.draw()
            except Exception as e:
                print("Error en la adquisición:", e)

    def guardar_datos(self):
    #"""Guarda los datos de la señal EMG en un archivo CSV con timestamp por muestra."""
        filename, _ = QFileDialog.getSaveFileName(self, "Guardar archivo", "", "Archivos CSV (*.csv)")
        if filename:
            if not filename.endswith(".csv"):
                filename += ".csv"  # Añadir extensión si el usuario no la incluye
            try:
                # Obtener la fecha y hora actual para cada muestra
                #tiempo_actual = datetime.now()
                #timestamps = [tiempo_actual.strftime("%Y-%m-%d %H:%M:%S")] * len(self.x)

                # Crear DataFrame con tiempo, señal y timestamp
                df = pd.DataFrame({
                    "Tiempo (s)": self.x,
                    "Voltaje (V)": self.y,
                    #"Fecha y Hora": timestamps
                })

                df.to_csv(filename, index=False)
                print("Datos guardados correctamente en:", filename)
            except Exception as e:
                print("Error al guardar el archivo:", e)
        else:
            print("No se especificó un archivo para guardar.")


    def mostrar_informacion(self):
        """Abre un archivo de texto con los datos guardados."""
        filename, _ = QFileDialog.getOpenFileName(self, "Abrir archivo de texto", "", "Archivos de texto (*.txt)")
        if filename:
            try:
                import subprocess
                subprocess.Popen(["notepad", filename])
                print("Archivo de texto abierto:", filename)
            except Exception as e:
                print("Error al abrir el archivo de texto:", e)
        else:
            print("No se especificó un archivo para abrir.")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    ventana = Principal()
    ventana.show()
    sys.exit(app.exec())


