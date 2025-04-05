import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from scipy.signal import butter, filtfilt

# Cargar la señal desde el archivo
file_path = "C:\\Users\\LENOVO\\Desktop\\SEXTO SEMESTRE\\PROCESAMIENTO DIGITAL DE SEÑALES\\LAB SEÑALES\\Cuarto lab\\arcdefdef.csv"
df = pd.read_csv(file_path)

# Extraer datos de tiempo y voltaje
tiempo = df.iloc[:, 0]
voltaje = df.iloc[:, 1]

# Estimar frecuencia de muestreo
fs_estimates = 1 / tiempo.diff().dropna().unique()
fs_mean = fs_estimates.mean()
print(f"Frecuencia de muestreo estimada: {fs_mean:.2f} Hz")

# Función de filtro Butterworth
def butterworth_filter(data, cutoff, fs, filter_type, order=4):
    nyquist = 0.5 * fs * 5
    normal_cutoff = cutoff / nyquist
    if not (0 < normal_cutoff < 1):
        raise ValueError(f"Error: Frecuencia de corte normalizada fuera de rango: {normal_cutoff}")
    b, a = butter(order, normal_cutoff, btype=filter_type, analog=False)
    return filtfilt(b, a, data)

# Aplicar filtros
filtered_high = butterworth_filter(voltaje, 20, fs_mean, 'high')
filtered_signal = butterworth_filter(filtered_high, 20, fs_mean, 'low')

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from scipy.signal import butter, filtfilt
from scipy.stats import t as t_dist

# Cargar la señal desde el archivo
file_path = "C:\\Users\\LENOVO\\Desktop\\SEXTO SEMESTRE\\PROCESAMIENTO DIGITAL DE SEÑALES\\LAB SEÑALES\\Cuarto lab\\arcdefdef.csv"
df = pd.read_csv(file_path)

# Extraer datos de tiempo y voltaje
tiempo = df.iloc[:, 0]
voltaje = df.iloc[:, 1]

# Estimar frecuencia de muestreo
fs_estimates = 1 / tiempo.diff().dropna().unique()
fs_mean = fs_estimates.mean()

# Filtro Butterworth (opcional si se quiere usar señal filtrada)
def butterworth_filter(data, cutoff, fs, filter_type, order=4):
    nyquist = 0.5 * fs * 5
    normal_cutoff = cutoff / nyquist
    if not (0 < normal_cutoff < 1):
        raise ValueError(f"Frecuencia de corte fuera de rango: {normal_cutoff}")
    b, a = butter(order, normal_cutoff, btype=filter_type, analog=False)
    return filtfilt(b, a, data)

# Aplicar filtro (si se usa señal filtrada para visualizar)
filtered_high = butterworth_filter(voltaje, 20, fs_mean, 'high')
filtered_signal = butterworth_filter(filtered_high, 20, fs_mean, 'low')

# -----------------------------
# CONTRACCIONES: análisis estadístico con señal ORIGINAL
# -----------------------------

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


# Estadístico t
H0 = mean1 - mean2
t = (mean1 - mean2) / np.sqrt((std1**2 / n1) + (std2**2 / n2))

# Grados de libertad y t crítico
df = min(n1 - 1, n2 - 1)
alpha = 0.05
t_crit = t_dist.ppf(1 - alpha / 2, df)

# Mostrar resultados
print("\n🧪 TEST DE DOS COLAS")
print(f"Contracción 1 (0-25s) -> Media: {mean1:.4f}, Desviación estándar: {std1:.4f}, n: {n1}")
print(f"Contracción 2 (60-80s) -> Media: {mean2:.4f}, Desviación estándar: {std2:.4f}, n: {n2}")
print(f"H0 (media1 - media2): {H0:.4f}")
print(f"Estadístico t: {t:.4f}")
print(f"t_crit (95% confianza, df={df}): ±{t_crit:.4f}")
print(f"Muestras totales en la señal: {len(voltaje)}")

# Graficar señal y regiones
plt.figure(figsize=(12, 5))
plt.plot(tiempo, filtered_signal, label="Señal EMG Filtrada", alpha=0.6)
plt.axvspan(0, 25, color='green', alpha=0.3, label="Contracción 1 (0-25s)")
plt.axvspan(60, 80, color='red', alpha=0.3, label="Contracción 2 (60-80s)")
plt.xlabel("Tiempo (s)")
plt.ylabel("Voltaje (V)")
plt.title("Señal EMG y Contracciones Analizadas")
plt.legend()
plt.grid(True)
plt.tight_layout()
plt.show()

# -----------------------------
# GRAFICAR TEST DE DOS COLAS
# -----------------------------

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
