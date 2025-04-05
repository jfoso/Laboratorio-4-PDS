# Laboratorio-4-PDS
## OBJETIVO
Aplicar técnicas de filtrado de señales continuas y análisis espectral a una señal electromiográfica (EMG) para identificar patrones asociados a la fatiga muscular, evaluando su contenido frecuencial mediante procesamiento digital de señales.
## Procedimiento
Para empezar a realizar nuestro laboratorio debemos tener en cuenta que es una EMG (Electromiograma). Esta es una grabación de la actividad eléctrica de los músculos (actividad mioeléctrica, en este caso se tomaran los datos mioelectricos mediante electrodos superficiales, utilizando dos electrodos activos y un electrodo referencia tierra ubicados en la piel sobre el músculo a evaluar, esta señal será la diferencia entre las señales medidas por los electrodos activos.Teniendo esto en cuenta, se colocaran los electrodos al músculo a analizar mediante una interfaz realizada en python donde se adquiere la señal emg y se capturan los datos obtenidos. Para obtener la señal deseada se le pedirà al sujeto que realice una contracción muscular continua hasta fatigar el músculo a evaluar para registrar la señal Emg en tiempo real en todo el proceso de la fatiga donde se obtuvo la siguiente señal:
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

### Aventanamiento
Posterior al filtrado de la señal se dividirá la señal registrada en ventanas de tiempo, en este caso se utilizo la tecnica de aventanamiento (poner tecnica usada) mediante el siguiente código realizado en python:
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
### Análisis Espectral
Despues de realizar el aventanamiento se realizará el análisis espectral de cada ventana utilizando la Transformada rapida de fourier (FFT) con la intención de obtener el espectro de frecuencias en intervalos específicos de la señal obtenida mediante el siguiente código:
```ruby
# Aplicar Transformada de Fourier (FFT) a cada ventana
fft_results = [np.fft.fft(w) for w in windowed_signals]
frequencies = np.fft.fftfreq(samples_per_window, d=1/fs_mean)
```
## Prueba de hipótesis
Se realizo la presente prueba de hipótesis para verificar si el cambio en la mediana es significativo estadísticamente de la siguiente manera:
```ruby
El codigo va aqui
```
## Resultados obtenidos
(tener en cuenta los siguientes aspectos:
*El cambio en la mediana es significativo?
*Evaluar la disminución de la frecuencia mediana en cada ventana como indicador de la fatiga.)
