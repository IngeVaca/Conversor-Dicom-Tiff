"""
Generador de CSV maestro del Dataset Unificado
Autor: Jhon Jaime Vaca Hincapié
Año: 2025

Descripción:
Recorre todas las imágenes TIFF en E:\Dataset_unificado,
extrae metadatos (nombre, dataset de origen, densidad mamaria, categoría BI-RADS)
y genera un archivo CSV consolidado.
"""

import os
import pandas as pd
import matplotlib.pyplot as plt

# --- Configuración ---
dataset_base = r"E:\Dataset_unificado"
csv_salida = r"E:\Dataset_unificado\dataset_maestro_metadata.csv"

# --- Inicialización ---
registros = []

# --- Recorremos todo el dataset ---
for root, _, files in os.walk(dataset_base):
    for file in files:
        if file.lower().endswith(".tiff"):
            partes = os.path.relpath(root, dataset_base).split(os.sep)
            if len(partes) >= 2:
                densidad = partes[0].replace("Densidad_", "")
                birads = partes[1].replace("Birads_", "")
                
                # Determinar dataset de origen por el prefijo del archivo
                nombre_lower = file.lower()
                if "inb" in nombre_lower:
                    origen = "INbreast"
                elif "cbis" in nombre_lower:
                    origen = "CBIS-DDSM"
                elif "mammo" in nombre_lower:
                    origen = "DrMammo"
                else:
                    origen = "Desconocido"

                registros.append({
                    "nombre_imagen": file,
                    "ruta_relativa": os.path.join(partes[0], partes[1], file),
                    "ruta_completa": os.path.join(root, file),
                    "origen_dataset": origen,
                    "densidad_mamaria": densidad,
                    "categoria_birads": birads
                })

# --- Convertir a DataFrame ---
df = pd.DataFrame(registros)

# --- Guardar CSV ---
df.to_csv(csv_salida, index=False, encoding="utf-8-sig")

# --- Resumen ---
print(f"\n CSV maestro generado correctamente: {csv_salida}")
print(f"Total de imágenes registradas: {len(df)}\n")

print("--- Distribución por dataset de origen ---")
print(df["origen_dataset"].value_counts(), "\n")

print("--- Distribución por densidad mamaria ---")
print(df["densidad_mamaria"].value_counts(), "\n")

print("--- Distribución por categoría BI-RADS ---")
print(df["categoria_birads"].value_counts(), "\n")


# -------------- Generación resumen visual de dataset unificado ----------------

base = r"E:\Dataset_unificado"

registros = []

# Recorrer todas las carpetas
for root, _, files in os.walk(base):
    for file in files:
        if file.lower().endswith(".tiff"):
            partes = os.path.relpath(root, base).split(os.sep)
            if len(partes) >= 2:
                densidad = partes[0].replace("Densidad_", "")
                birads = partes[1].replace("Birads_", "")
                registros.append({"densidad_mamaria": densidad, "categoria_birads": birads})

# Crear DataFrame
df = pd.DataFrame(registros)

# Resumen por densidad y BI-RADS
resumen = df.groupby(["densidad_mamaria", "categoria_birads"]).size().unstack(fill_value=0)
print("\n--- Distribución global de imágenes ---")
print(resumen)

# Graficar mapa de calor
plt.figure(figsize=(10, 6))
plt.title("Distribución global del Dataset Unificado (Densidad vs BI-RADS)", fontsize=14)
plt.xlabel("Categoría BI-RADS")
plt.ylabel("Densidad Mamaria")
plt.imshow(resumen.values, cmap="YlGnBu", aspect="auto")
plt.xticks(range(len(resumen.columns)), resumen.columns)
plt.yticks(range(len(resumen.index)), resumen.index)
plt.colorbar(label="Cantidad de imágenes")
for i, dens in enumerate(resumen.index):
    for j, birads in enumerate(resumen.columns):
        plt.text(j, i, resumen.iloc[i, j], ha='center', va='center', color='black', fontsize=8)
plt.tight_layout()
plt.show()
