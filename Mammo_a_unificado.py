"""
Mover archivos TIFF de DrMammo al Dataset Unificado
Autor: Jhon Jaime Vaca Hincapié
Año: 2025

Descripción:
Mueve las imágenes desde E:\Dataset_Mammo hacia E:\Dataset_unificado,
manteniendo la estructura de carpetas (Densidad/Birads).
No sobrescribe archivos existentes.
"""

import os
import shutil
import pandas as pd

# --- Configuración ---
origen = r"E:\Dataset_Mammo" # Esta ruta debe ser la del directorio donde se guardaron los TIFF
destino = r"E:\Dataset_unificado" # Ruta donde se encuentra el dataset unifciado
csv_salida = r"E:\Dataset_unificado\registro_movimiento_mammo.csv"

registros = []
total, movidos, errores = 0, 0, 0

print("Iniciando movimiento de archivos...\n")

for root, _, files in os.walk(origen):
    for file in files:
        if file.lower().endswith(".tiff"):
            total += 1
            ruta_origen = os.path.join(root, file)
            estructura_relativa = os.path.relpath(root, origen)
            ruta_destino = os.path.join(destino, estructura_relativa)
            os.makedirs(ruta_destino, exist_ok=True)
            ruta_final = os.path.join(ruta_destino, file)

            try:
                if not os.path.exists(ruta_final):
                    shutil.move(ruta_origen, ruta_final)
                    movidos += 1

                    partes = estructura_relativa.split(os.sep)
                    densidad = partes[0].replace("Densidad_", "") if len(partes) > 0 else "?"
                    birads = partes[1].replace("Birads_", "") if len(partes) > 1 else "?"

                    registros.append({
                        "archivo": file,
                        "ruta_origen": ruta_origen,
                        "ruta_destino": ruta_final,
                        "densidad_mamaria": densidad,
                        "categoria_birads": birads
                    })
                else:
                    print(f"Archivo ya existente, omitido: {file}")

            except Exception as e:
                print(f"Error al mover {file}: {e}")
                errores += 1

# Guardar registro CSV
df = pd.DataFrame(registros)
df.to_csv(csv_salida, index=False, encoding="utf-8-sig")

print("\n--- Resumen del proceso ---")
print(f"Total encontrados: {total}")
print(f"Movidos correctamente: {movidos}")
print(f"Errores: {errores}")
print(f"CSV de trazabilidad: {csv_salida}")
