# Laboratorio-4-PDS
## OBJETIVO
Aplicar técnicas de filtrado de señales continuas y análisis espectral a una señal electromiográfica (EMG) para identificar patrones asociados a la fatiga muscular, evaluando su contenido frecuencial mediante procesamiento digital de señales.
## Procedimiento
Para empezar a realizar nuestro laboratorio debemos tener en cuenta que es una EMG (Electromiograma). Esta es una grabación de la actividad eléctrica de los músculos (actividad mioeléctrica, en este caso se tomaran los datos mioelectricos mediante electrodos superficiales, utilizando dos electrodos activos y un electrodo referencia tierra ubicados en la piel sobre el músculo a evaluar, esta señal será la diferencia entre las señales medidas por los electrodos activos.Teniendo esto en cuenta, se colocaran los electrodos al músculo a analizar mediante una interfaz realizada en python donde se adquiere la señal emg y se capturan los datos obtenidos. Para obtener la señal deseada se le pedirà al sujeto que realice una contracción muscular continua hasta fatigar el músculo a evaluar para registrar la señal Emg en tiempo real en todo el proceso de la fatiga donde se obtuvo la siguiente señal:
(foto de la señal).
Posterior a esto se procesará la señal obtenida de la siguiente manera:
### Filtrado de la señal
Se realizó mediante el siguiente codigo un filtro pasa altas con la intención de eliminar los componentes de bajas frecuencias y un filtro pasa bajas para eliminar las frecuencias altas no deseadas para evitar posibles interferencias causadas por ruidos externos.
```ruby
El codigo va aqui
```

### Aventanamiento
Posterior al filtrado de la señal se dividirá la señal registrada en ventanas de tiempo, en este caso se utilizo la tecnica de aventanamiento (poner tecnica usada) mediante el siguiente código realizado en python:
```ruby
El codigo va aqui
```
### Análisis Espectral
Despues de realizar el aventanamiento se realizará el análisis espectral de cada ventana utilizando la Transformada rapida de fourier (FFT) con la intención de obtener el espectro de frecuencias en intervalos específicos de la señal obtenida mediante el siguiente código:
```ruby
El codigo va aqui
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
