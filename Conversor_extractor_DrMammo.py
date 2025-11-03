"""
Conversor DrMammo (VINDr-Mammo) a TIFF estructurado - versión final
Autor: Jhon Jaime Vaca Hincapié
Correo: jjvacah@libertadores.edu.co
ORCID: https://orcid.org/0009-0007-7994-3130
Maestría en Ingeniería – Fundación Universitaria Los Libertadores
Año: 2025

Descripción:
Convierte imágenes del dataset DrMammo en formato DICOM a TIFF (16 bits sin compresión),
organizando las imágenes en carpetas según densidad mamaria y categoría BI-RADS.
Utiliza 'id_estudio' como identificador de carpeta.
Genera un CSV con las rutas originales y finales.
"""

import os
import pydicom
from PIL import Image
import numpy as np
import pandas as pd
from tqdm import tqdm
# Directorios
base_dicom = r"E:\DrMammo\images"       # Carpeta base de imágenes DICOM
base_salida = r"D:\Dataset_Mammo"       # Carpeta donde se guardarán los TIFF
csv_in = "metadata_filtrado_VINDr_es (2).csv"  # CSV filtrado
csv_out = "metadata_Mammo_convertido.csv"      # CSV de salida

# Pasos iniciales

def normalizar_a_16bits(imagen):
    """Normaliza la imagen a rango 0-65535 (16 bits)."""
    imagen = imagen.astype(np.float32)
    imagen -= np.min(imagen)
    max_val = np.max(imagen)
    if max_val > 0:
        imagen /= max_val
    return (imagen * 65535).astype(np.uint16)

def convertir_y_guardar(ruta_dcm, ruta_salida):
    """Lee un archivo DICOM, lo normaliza y lo guarda como TIFF."""
    try:
        dcm = pydicom.dcmread(ruta_dcm)
        img = dcm.pixel_array.astype(np.float32)

        # Corregir inversión fotométrica si aplica
        if hasattr(dcm, "PhotometricInterpretation") and dcm.PhotometricInterpretation == "MONOCHROME1":
            img = np.max(img) - img

        img_16 = normalizar_a_16bits(img)
        Image.fromarray(img_16).save(ruta_salida)
        return True
    except Exception as e:
        print(f"Error procesando {ruta_dcm}: {e}")
        return False

def crear_estructura_salida(densidad, birads):
    """Crea carpetas Densidad_X/Birads_Y si no existen."""
    carpeta = os.path.join(base_salida, f"Densidad_{densidad}", f"Birads_{int(birads)}")
    os.makedirs(carpeta, exist_ok=True)
    return carpeta

# Recolección y ubicación datos

df = pd.read_csv(csv_in)
df.columns = [c.strip().lower() for c in df.columns]

if not {"id_estudio", "densidad_mamaria", "categoria_birads"}.issubset(df.columns):
    raise ValueError("El CSV debe contener las columnas: id_estudio, densidad_mamaria, categoria_birads")

resultados = []

print("\n--- Iniciando conversión DrMammo ---")

for idx, fila in tqdm(df.iterrows(), total=len(df), desc="Procesando estudios", unit="estudio"):
    study_id = str(fila["id_estudio"]).strip()
    densidad = str(fila["densidad_mamaria"]).strip().upper()
    birads = int(fila["categoria_birads"])

    carpeta_dicom = os.path.join(base_dicom, study_id)
    if not os.path.isdir(carpeta_dicom):
        continue  # si la carpeta no existe, se omite

    carpeta_salida = crear_estructura_salida(densidad, birads)
    archivos_dcm = [f for f in os.listdir(carpeta_dicom) if f.lower().endswith((".dcm", ".dicom"))]

    contador = 1
    for archivo in archivos_dcm:
        ruta_dcm = os.path.join(carpeta_dicom, archivo)
        nombre_salida = f"MAMMO_P{idx:05d}_{study_id}_{contador}.tiff"
        ruta_salida = os.path.join(carpeta_salida, nombre_salida)

        ok = convertir_y_guardar(ruta_dcm, ruta_salida)
        if ok:
            resultados.append({
                "id_estudio": study_id,
                "archivo_original": ruta_dcm,
                "archivo_tiff": ruta_salida,
                "densidad_mamaria": densidad,
                "categoria_birads": birads
            })
            contador += 1

# CSV resumen

df_resultados = pd.DataFrame(resultados)
df_resultados.to_csv(csv_out, index=False, encoding="utf-8-sig")

print(f"\nConversión completada. Total imágenes convertidas: {len(df_resultados)}")
print(f"Archivo CSV guardado en: {csv_out}")
