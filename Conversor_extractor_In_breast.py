"""
Conversor y organizador de imágenes INbreast según estructura jerárquica
Autor: Jhon Jaime Vaca Hincapié
Proyecto Maestría en Ingeniería Automática
Año: 2025

Descripción:
Convierte los archivos DICOM de INbreast a TIFF de 16 bits, aplicando
normalización e inversión fotométrica cuando es necesario.
Organiza las imágenes según la estructura:

Dataset_unificado/
│
├── Densidad_A/
│   ├── Birads_0/
│   ├── Birads_1/
│   ├── ...
│
└── Densidad_D/
    ├── Birads_0/
    ├── Birads_1/
    ├── ...
"""

import os
import pandas as pd
import numpy as np
from PIL import Image
import pydicom

# Directorios
csv_in = r"metadata_filtrado_INbreast_es (2).csv"       # CSV con metadatos filtrados
dicom_folder = r"E:\INbreast Release 1.0\AllDICOMs"        # Carpeta donde están los DICOM
output_root = r"D:\Dataset_unificado"                      # Carpeta raíz donde se guardarán los TIFF
csv_out = r"D:\metadata_INbreast_convertido.csv"           # CSV de salida con las imágenes procesadas

# CSV filtrados
df = pd.read_csv(csv_in)
df.columns = [c.strip().lower() for c in df.columns]

print(f"Total de registros en CSV: {len(df)}")
print("Columnas detectadas:", list(df.columns))

# Verificación de columnas necesarias
cols_req = ["id_paciente", "id_imagen", "densidad_mamaria", "categoria_birads"]
for col in cols_req:
    if col not in df.columns:
        raise ValueError(f"Falta la columna requerida: {col}")

# Elaboración estructura carpetas
for densidad in ["A", "B", "C", "D"]:
    for birads in range(0, 7):
        folder_path = os.path.join(output_root, f"Densidad_{densidad}", f"Birads_{birads}")
        os.makedirs(folder_path, exist_ok=True)

# Lectura de imágenes DICOM

registros_convertidos = []

for idx, row in df.iterrows():
    try:
        densidad = str(row["densidad_mamaria"]).upper()
        birads = int(float(row["categoria_birads"]))
        paciente = f"P{idx+1:04d}"
        id_img = str(row["id_imagen"]).strip()

        # Buscar el archivo DICOM correspondiente (usa coincidencia parcial)
        matching_files = [f for f in os.listdir(dicom_folder) if f.startswith(str(id_img))]
        if not matching_files:
            print(f"[ADVERTENCIA] No se encontró archivo para ID: {id_img}")
            continue

        dicom_file = matching_files[0]  # Toma el primero que coincida
        dicom_path = os.path.join(dicom_folder, dicom_file)

        # Leer imagen DICOM
        dcm = pydicom.dcmread(dicom_path)
        image = dcm.pixel_array.astype(np.float32)

        # Corregir inversión fotométrica si aplica
        if hasattr(dcm, "PhotometricInterpretation") and dcm.PhotometricInterpretation == "MONOCHROME1":
            image = np.max(image) - image

        # Normalización a 16 bits
        image = (image - np.min(image)) / (np.max(image) - np.min(image))
        image = (image * 65535).astype(np.uint16)

        # Carpeta destino
        output_folder = os.path.join(output_root, f"Densidad_{densidad}", f"Birads_{birads}")
        os.makedirs(output_folder, exist_ok=True)

        # Nombre del archivo TIFF
        output_name = f"INB_{paciente}_{id_img}.tiff"
        output_path = os.path.join(output_folder, output_name)

        # Guardar como TIFF
        Image.fromarray(image).save(output_path)

        registros_convertidos.append({
            "id_paciente": paciente,
            "id_imagen": id_img,
            "densidad_mamaria": densidad,
            "categoria_birads": birads,
            "ruta_original": dicom_path,
            "ruta_tiff": output_path
        })

        print(f"[OK] Convertido: {output_name}")

    except Exception as e:
        print(f"[ERROR] No se pudo procesar {row['id_imagen']}: {e}")

# Resumen en CSV

df_out = pd.DataFrame(registros_convertidos)
df_out.to_csv(csv_out, index=False)
print(f"\nConversión finalizada. Total de imágenes convertidas: {len(df_out)}")
print(f"CSV de salida guardado en: {csv_out}")
