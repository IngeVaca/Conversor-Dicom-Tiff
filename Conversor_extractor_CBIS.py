"""
Conversor CBIS-DDSM a TIFF estructurado 
Autor: Jhon Jaime Vaca Hincapié
Correo: jjvacah@libertadores.edu.co
Maestría en Ingeniería – Fundación Universitaria Los Libertadores
Año: 2025
"""

import os
import pandas as pd
import numpy as np
import pydicom
from PIL import Image
from tqdm import tqdm

# === CONFIGURACIÓN ===
base_input = r"C:\Users\Jhon\Desktop\manifest-ZkhPvrLo5216730872708713142"
base_output = r"D:\Dataset_CBIS"
csv_in = "metadata_filtrado_CBIS_es (2).csv"
csv_out = "metadata_CBIS_convertido.csv"

# Crear estructura base
for densidad in ["A", "B", "C", "D"]:
    for birads in ["0", "1", "2", "3", "4", "5", "6"]:
        os.makedirs(os.path.join(base_output, f"Densidad_{densidad}", f"Birads_{birads}"), exist_ok=True)

# Leer CSV
df = pd.read_csv(csv_in)
df.columns = [c.strip().lower() for c in df.columns]

resultados = []
errores = []

# --- Función de procesamiento individual ---
def procesar_imagen(idx, data):
    try:
        id_paciente = str(data.get("id_paciente", f"P_{idx:04d}"))
        ruta_imagen = str(data.get("imagen_id", ""))
        densidad = str(data.get("densidad_mamaria", "ND")).strip().upper()
        birads = str(int(data.get("categoria_birads", 0))) if not pd.isna(data.get("categoria_birads")) else "0"

        # Buscar archivo DICOM (coincidencia parcial)
        found_dicom = None
        for root, _, files in os.walk(base_input):
            for file in files:
                if file.lower().endswith((".dcm", ".dicom")) and ruta_imagen.split("/")[0] in root:
                    found_dicom = os.path.join(root, file)
                    break
            if found_dicom:
                break

        if not found_dicom:
            errores.append((idx, "Archivo no encontrado"))
            return None

        # Leer DICOM
        try:
            dcm = pydicom.dcmread(found_dicom, force=True)
            image = dcm.pixel_array.astype(np.float32)
        except Exception as e:
            errores.append((idx, f"Error lectura DICOM: {e}"))
            return None

        # Corregir fotometría
        if hasattr(dcm, "PhotometricInterpretation") and dcm.PhotometricInterpretation == "MONOCHROME1":
            image = np.max(image) - image

        # Normalización
        min_val, max_val = np.min(image), np.max(image)
        if max_val == min_val or np.isnan(max_val) or np.isnan(min_val):
            errores.append((idx, "Valores NaN o constantes"))
            return None

        image = (image - min_val) / (max_val - min_val)
        image = (image * 65535).astype(np.uint16)

        # Destino
        output_dir = os.path.join(base_output, f"Densidad_{densidad}", f"Birads_{birads}")
        os.makedirs(output_dir, exist_ok=True)

        vista = ruta_imagen.split("_")[-1].replace(".dcm", "")
        tiff_name = f"CBIS_{id_paciente}_{vista}_{idx+1}.tiff"
        tiff_path = os.path.join(output_dir, tiff_name)

        Image.fromarray(image).save(tiff_path, compression=None)

        return {
            "id_paciente": id_paciente,
            "densidad_mamaria": densidad,
            "categoria_birads": birads,
            "ruta_origen": found_dicom,
            "ruta_tiff": tiff_path,
            "fuente_datos": "CBIS-DDSM"
        }

    except Exception as e:
        errores.append((idx, str(e)))
        return None


# --- Procesamiento secuencial con barra de progreso ---
for i, row in tqdm(df.iterrows(), total=len(df), desc="Convirtiendo imágenes", unit="img"):
    resultado = procesar_imagen(i, row)
    if resultado is not None:
        resultados.append(resultado)

# --- Guardar CSV final ---
if resultados:
    df_out = pd.DataFrame(resultados)
    df_out.to_csv(csv_out, index=False, encoding="utf-8")
    print(f"\nConversión finalizada correctamente.")
    print(f"Imágenes convertidas: {len(df_out)}")
    print(f"Archivo guardado: {csv_out}")
