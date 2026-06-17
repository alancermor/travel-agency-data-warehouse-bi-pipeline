# %%
import pandas as pd
import random

print("Arreglando el archivo sin correr todo desde cero...")

# 1. Leemos tus CSVs que ya están guardados
df_ventas = pd.read_csv('fact_ventas.csv')
df_agentes = pd.read_csv('dim_agentes.csv')

# 2. Sacamos la lista de agentes y se la asignamos al azar
lista_agentes = df_agentes['id_agente'].tolist()
df_ventas['id_agente'] = [random.choice(lista_agentes) for _ in range(len(df_ventas))]

# 3. Sobrescribimos el archivo fact_ventas.csv
df_ventas.to_csv('fact_ventas.csv', index=False, encoding='utf-8')

print("¡Listo! Ya tienes agentes en tus ventas.")
# %%
# %%
import pandas as pd
import random

print("Calculando los dineros...")

# 1. Leemos el archivo actual (el que ya tiene a los agentes)
df_ventas = pd.read_csv('fact_ventas.csv')

# 2. Como no tenemos precios reales de los catálogos en este histórico, 
# vamos a simular el Precio de Venta Total (ej. viajes entre $5,000 y $50,000)
df_ventas['precio_venta_total'] = [round(random.uniform(5000, 50000), 2) for _ in range(len(df_ventas))]

# Simulamos que el proveedor (hotel/aerolínea) nos cobra entre el 70% y el 85% de ese precio
df_ventas['costo_proveedor'] = df_ventas['precio_venta_total'] * [round(random.uniform(0.70, 0.85), 2) for _ in range(len(df_ventas))]

# 3. Ahora sí, tus matemáticas:
# Margen de la agencia (Lo que queda en caja después de pagarle al proveedor)
df_ventas['margen_agencia'] = df_ventas['precio_venta_total'] - df_ventas['costo_proveedor']

# Comisión del agente (El 30% de ese margen, justo como pediste)
df_ventas['comision_agente'] = df_ventas['margen_agencia'] * 0.30

# Utilidad neta (Lo que se embolsa la empresa al final del día)
df_ventas['utilidad_neta_empresa'] = df_ventas['margen_agencia'] - df_ventas['comision_agente']

# 4. Redondeamos a 2 decimales para que parezca dinero real y no se vea feo en Power BI
columnas_dinero = ['costo_proveedor', 'margen_agencia', 'comision_agente', 'utilidad_neta_empresa']
df_ventas[columnas_dinero] = df_ventas[columnas_dinero].round(2)

# 5. Sobrescribimos el archivo fact_ventas.csv
df_ventas.to_csv('fact_ventas.csv', index=False, encoding='utf-8')

print("¡Listo el músculo financiero! Ya tienes ventas, márgenes y comisiones en tu CSV.")
#%%