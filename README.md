# Sales-Prediction-Analytics

Este repositorio contiene un sistema de predicción de ventas utilizando modelos ARIMA para analizar datos transaccionales generados sintéticamente. El proyecto incluye:

Generación de datos sintéticos (generator.py):

Simula transacciones multi-item y single-item con correlaciones entre productos.

Configurable por fecha, volumen de datos y formato de salida (CSV/Parquet).

Modelado predictivo (main.py):

Predice ventas futuras por canal (Online, In-Store, Mobile) usando ARIMA.

Calcula intervalos de confianza y métricas de certeza para cada predicción.

Datos de referencia (channels.csv):

Mapeo de IDs de canales a nombres descriptivos.

🛠️ Tecnologías
Python 3.10+

Pandas (manipulación de datos)

Statsmodels (ARIMA)

PyArrow (Parquet)

NumPy (cálculos numéricos)


