"""
Mover imágenes TIFF de CBIS a Dataset_unificado (sin sobrescribir)
Autor: Jhon Jaime Vaca Hincapié
Descripción:
   - Mueve los archivos TIFF desde D:\Dataset_CBIS hacia D:\Dataset_unificado
   - Mantiene la estructura de densidad y BI-RADS
   - No sobrescribe imágenes existentes (por ejemplo, las de INbreast)
   - No duplica espacio
"""

import os
import shutil

# --- Directorios principales ---
origen_base = r"D:\Dataset_CBIS" # Esta ruta debe ser asignada al directorio donde se guardaron los TIFF de CBIS
destino_base = r"D:\Dataset_unificado" # Esta ruta debe ser asignada al directorio donde se guarda el dataset unificado

# --- Recorrer estructura ---
for root, dirs, files in os.walk(origen_base):
    for file in files:
        if file.lower().endswith((".tif", ".tiff")):
            ruta_origen = os.path.join(root, file)

            # Calcular ruta relativa (mantiene Densidad_X/Birads_Y)
            ruta_relativa = os.path.relpath(root, origen_base)
            ruta_destino = os.path.join(destino_base, ruta_relativa)

            # Asegurar que el destino exista
            os.makedirs(ruta_destino, exist_ok=True)

            # Ruta final del archivo
            destino_final = os.path.join(ruta_destino, file)

            # Verificar si ya existe un archivo con el mismo nombre
            if os.path.exists(destino_final):
                print(f"Archivo existente, omitido: {destino_final}")
                continue

            # Mover archivo
            try:
                shutil.move(ruta_origen, destino_final)
                print(f"Movido: {ruta_origen} → {destino_final}")
            except Exception as e:
                print(f"Error al mover {ruta_origen}: {e}")

print("\nMovimiento completado correctamente. No se sobrescribieron archivos existentes.")
