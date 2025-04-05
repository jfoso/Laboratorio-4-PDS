# Laboratorio-4-PDS
## OBJETIVO
Aplicar técnicas de filtrado de señales continuas y análisis espectral a una señal electromiográfica (EMG) para identificar patrones asociados a la fatiga muscular, evaluando su contenido frecuencial mediante procesamiento digital de señales.
## Procedimiento
Para empezar a realizar nuestro laboratorio debemos tener en cuenta que es una EMG (Electromiograma). Esta es una grabación de la actividad eléctrica de los músculos (actividad mioeléctrica, en este caso se tomaran los datos mioelectricos mediante electrodos superficiales, utilizando dos electrodos activos y un electrodo referencia tierra ubicados en la piel sobre el músculo a evaluar, esta señal será la diferencia entre las señales medidas por los electrodos activos.Teniendo esto en cuenta, se colocaran los electrodos al músculo a analizar mediante una interfaz realizada en python donde se adquiere la señal emg y se capturan los datos obtenidos. Para obtener la señal deseada se le pedirà al sujeto que realice una contracción muscular continua hasta fatigar el músculo a evaluar para registrar la señal Emg en tiempo real en todo el proceso de la fatiga donde se obtuvo la siguiente señal:
```ruby
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
```
![Imagen de WhatsApp 2025-04-04 a las 17 05 28_6ea5332a](https://github.com/user-attachments/assets/89cabc90-b14f-4c3c-b3a3-4ca1a3dfca8f)

Posterior a esto se procesará la señal obtenida de la siguiente manera:
### Filtrado de la señal
Se realizó mediante el siguiente codigo un filtro pasa altas con la intención de eliminar los componentes de bajas frecuencias y un filtro pasa bajas para eliminar las frecuencias altas no deseadas para evitar posibles interferencias causadas por ruidos externos.
```ruby
# Función para diseñar y aplicar un filtro Butterworth
def butterworth_filter(data, cutoff, fs, filter_type, order=4):
    nyquist = 0.5 * fs * 5 # Frecuencia de Nyquist
    normal_cutoff = cutoff / nyquist
    if not(0 < normal_cutoff < 1): # Normalizar la frecuencia de corte
        raise ValueError(f"Error: La frecuencia de corte normalizada debe ser un valor entre 0 y 1. Valor actual:{normal_cutoff}")
    b, a = butter(order, normal_cutoff, btype=filter_type, analog=False)
    return filtfilt(b, a, data)

# Aplicar filtro pasa altas (10 Hz)
filtered_high = butterworth_filter(voltaje, 20, fs_mean, 'high')

# Aplicar filtro pasa bajas (60 Hz)
filtered_signal = butterworth_filter(filtered_high, 20, fs_mean, 'low')
```
![Imagen de WhatsApp 2025-04-04 a las 17 05 47_d314aa91](https://github.com/user-attachments/assets/901fc222-9c4f-4533-8ceb-4c04e34b07ae)

### Aventanamiento
Posterior al filtrado de la señal se dividirá la señal registrada en ventanas de tiempo, en este caso se utilizo la tecnica de aventanamiento hamming mediante el siguiente código realizado en python:
```ruby
# Definir tamaño de ventana en segundos
window_size = 1  # 1 segundo por ventana
samples_per_window = int(window_size * fs_mean)  # Convertir a muestras

# Aplicar aventanamiento
num_windows = len(filtered_signal) // samples_per_window
windows = [filtered_signal[i * samples_per_window:(i + 1) * samples_per_window] for i in range(num_windows)]

# Aplicar ventana de Hamming
windowed_signals = [w * np.hamming(len(w)) for w in windows]
```
![Imagen de WhatsApp 2025-04-04 a las 17 06 09_42064d30](https://github.com/user-attachments/assets/a84f1096-dcc6-48ee-ae4e-900eaa23eb63)

### Análisis Espectral
Despues de realizar el aventanamiento se realizará el análisis espectral de cada ventana utilizando la Transformada rapida de fourier (FFT) con la intención de obtener el espectro de frecuencias en intervalos específicos de la señal obtenida mediante el siguiente código:
```ruby
# Aplicar Transformada de Fourier (FFT) a cada ventana
fft_results = [np.fft.fft(w) for w in windowed_signals]
frequencies = np.fft.fftfreq(samples_per_window, d=1/fs_mean)
```
![Imagen de WhatsApp 2025-04-04 a las 17 06 38_fb3093bf](https://github.com/user-attachments/assets/4dd12541-c2a5-412b-b1a0-43e7b39db01e)

## Prueba de hipótesis
Se realizo la presente prueba de hipótesis para verificar si el cambio en la mediana es significativo estadísticamente.
Inicialmente se tomaron la primer y última contracción para así poder obtener los estadísticos de cada una. 
```ruby
# Contracción 1 (0-20s)
mask1 = (tiempo >= 0) & (tiempo <= 25)
contraction1 = voltaje[mask1]
n1 = len(contraction1)
mean1 = np.mean(contraction1)
std1 = np.std(contraction1, ddof=1)

# Contracción 2 (60-80s)
mask2 = (tiempo >= 60) & (tiempo <= 80)
contraction2 = voltaje[mask2]
n2 = len(contraction2)
mean2 = np.mean(contraction2)
std2 = np.std(contraction2, ddof=1)
```
Posterior a esto se calculo el t para posicionarlo en la gráfica y así poder saber si se rechaza la hipótesis nula, también se hallo el tcrit para saber delimitar cada cola.
```ruby
t = (mean1 - mean2) / np.sqrt((std1**2 / n1) + (std2**2 / n2))
t_crit = t_dist.ppf(1 - alpha / 2, df)
```
Para poder visualizar de forma más clara el resultado de nuetsro t calculado respecto a los demás valores, se hizo una gráfica que tuviera todos los valores calculados relacionados entre si. 
```ruby
# Rango para eje x (valores t)
t_vals = np.linspace(-4, 4, 400)
pdf_vals = t_dist.pdf(t_vals, df)

plt.figure(figsize=(10, 4))
plt.plot(t_vals, pdf_vals, label=f'Distribución t (df={df})', color='black')
plt.axvline(t_crit, color='red', linestyle='--', label=f't_crit = ±{t_crit:.2f}')
plt.axvline(-t_crit, color='red', linestyle='--')
plt.axvline(t, color='blue', linestyle='-', linewidth=2, label=f'Estadístico t = {t:.2f}')

# Sombrear regiones de rechazo
plt.fill_between(t_vals, 0, pdf_vals, where=(t_vals >= t_crit), color='red', alpha=0.2)
plt.fill_between(t_vals, 0, pdf_vals, where=(t_vals <= -t_crit), color='red', alpha=0.2)

plt.title("Test de dos colas (Nivel de significancia 5%)")
plt.xlabel("t")
plt.ylabel("Densidad de probabilidad")
plt.legend()
plt.grid(True)
plt.tight_layout()
plt.show()
```
## Resultados obtenidos
* La señal original (Fig. "Señal EMG Original") muestra variaciones de voltaje en el tiempo, con amplitudes entre 0.80 V y 0.84 V, correspondientes a la actividad mioeléctrica del músculo.
* El espectro de frecuencia (Fig. "Espectro de Frecuencia de la Señal EMG") revela componentes frecuenciales dominantes en el rango típico de señales EMG entre 20 y 500Hz, con magnitudes entre 0.00005 y 0.00035 V.
* El análisis espectral permitió identificar cambios en la distribución de frecuencias de la señal EMG, donde un incremento en componentes de baja frecuencia y una reducción en la amplitud pueden ser indicativos de fatiga muscular.
* Respecto al análisis de hipótesis se puede evidenciar que el valor de t se encuentra fuera de la grafica puede ser debido a que el valor de las muestras es muy grande respecto a las desviaciones estándar, generando que el valor de t sea grande. Además de esto se evidencia que el valor de las media no es el mismo. 

