import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from scipy.signal import butter, filtfilt

# Cargar la señal EMG desde un archivo CSV
file_path = "C:\\Users\\sachi\\OneDrive - unimilitar.edu.co\\Sexto semestre\\Lab señales\\arcdefdef.csv"  # Asegúrate de que el archivo esté en el mismo directorio
df = pd.read_csv(file_path)

# Extraer datos
tiempo = df.iloc[:, 0]  # Primera columna (Tiempo)
#tiempo = tiempo.astype(float)
voltaje = df.iloc[:, 1]  # Segunda columna (Voltaje)

# Estimar la frecuencia de muestreo (fs)
fs_estimates = 1 / tiempo.diff().dropna().unique()
fs_mean = fs_estimates.mean()  # Tomar un valor promedio si hay variaciones

# Graficar la señal original
plt.figure(figsize=(10, 4))
plt.plot(tiempo, voltaje, label="Señal EMG", color="b")
plt.xlabel("Tiempo (s)")
plt.ylabel("Voltaje (V)")
plt.title("Señal EMG Original")
plt.legend()
plt.grid(True)
plt.show()

print(f"Frecuencia de muestreo estimada: {fs_mean:.2f} Hz")

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


# Graficar señal original vs filtrada
plt.figure(figsize=(10, 4))
plt.plot(tiempo, voltaje, label="Señal Original", alpha=0.5, color="gray")
plt.plot(tiempo, filtered_signal, label="Señal Filtrada", color="blue")
plt.xlabel("Tiempo (s)")
plt.ylabel("Voltaje (V)")
plt.title("Señal EMG antes y después del filtrado")
plt.legend()
plt.grid(True)
plt.show()

# Definir tamaño de ventana en segundos
window_size = 1  # 1 segundo por ventana
samples_per_window = int(window_size * fs_mean)  # Convertir a muestras

# Aplicar aventanamiento
num_windows = len(filtered_signal) // samples_per_window
windows = [filtered_signal[i * samples_per_window:(i + 1) * samples_per_window] for i in range(num_windows)]

# Aplicar ventana de Hamming
windowed_signals = [w * np.hamming(len(w)) for w in windows]

# Graficar algunas ventanas
plt.figure(figsize=(10, 4))
for i in range(min(5, len(windowed_signals))):
    plt.plot(windowed_signals[i], label=f'Ventana {i+1}')
plt.xlabel("Muestras")
plt.ylabel("Voltaje (V)")
plt.title("Señales EMG con ventana de Hamming")
plt.legend()
plt.grid(True)
plt.show()

# Aplicar Transformada de Fourier (FFT) a cada ventana
fft_results = [np.fft.fft(w) for w in windowed_signals]
frequencies = np.fft.fftfreq(samples_per_window, d=1/fs_mean)

# Tomar solo la mitad del espectro (parte positiva)
half_spectrum = samples_per_window // 2
frequencies = frequencies[:half_spectrum]
fft_magnitudes = [np.abs(fft[:half_spectrum]) for fft in fft_results]

# Graficar el espectro de frecuencia de algunas ventanas
plt.figure(figsize=(10, 4))
for i in range(min(5, len(fft_magnitudes))):
    plt.plot(frequencies, fft_magnitudes[i], label=f'Ventana {i+1}')
plt.xlabel("Frecuencia (Hz)")
plt.ylabel("Magnitud")
plt.title("Espectro de Frecuencia de la Señal EMG")
plt.legend()
plt.grid(True)
plt.show()
