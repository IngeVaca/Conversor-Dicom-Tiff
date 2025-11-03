# Conversión y organización de imágenes DICOM a TIFF usando CSV filtrados

**Autor:** Jhon Jaime Vaca Hincapié  
**Correo:** jjvacah@libertadores.edu.co  
**ORCID:** [0009-0007-7994-3130](https://orcid.org/0009-0007-7994-3130)  
**Programa:** Maestría en Ingeniería – Énfasis en Ingeniería Automática  
**Institución:** Fundación Universitaria Los Libertadores  
**Año:** 2025  

## Descripción del proyecto

Este repositorio contiene los scripts utilizados para convertir las imágenes DICOM de INbreast, CBIS-DDSM y DrMammo a imágenes en formato TIFF. Además, se organizan las imágenes con la siguiente estructura:

Dataset_unificado\
  Densidad A\
     Bi-Rads 0\
     Bi-Rads 1\
     Bi-Rads 2\
     Bi-Rads 3\
     Bi-Rads 4\
     Bi-Rads 5\
     Bi-Rads 6\
  Densidad B\
     Bi-Rads 0\
     Bi-Rads 1\
     Bi-Rads 2\
     Bi-Rads 3\
     Bi-Rads 4\
     Bi-Rads 5\
     Bi-Rads 6\
 Densidad C\
     Bi-Rads 0\
     Bi-Rads 1\
     Bi-Rads 2\
     Bi-Rads 3\
     Bi-Rads 4\
     Bi-Rads 5\
     Bi-Rads 6\
Densidad D\
     Bi-Rads 0\
     Bi-Rads 1\
     Bi-Rads 2\
     Bi-Rads 3\
     Bi-Rads 4\
     Bi-Rads 5\
     Bi-Rads 6\


Para la selección de las imágenes se utilizan los siguientes CSV prefiltrados: 

- metadata_filtrado_CBIS_es.csv
- metadata_filtrado_VINDr_es.csv
- metadata_filtrado_INbreast_es.csv

Es importante mencionar que los datasets deben estar descargados previamente. Además, los scripts fueron diseñados para ser usados en Jupyter o en cualquier editor de código que se ejecute de manera local (no funcionan en Colab).  

El primer script que se debe ejecutar es:  

**Conversor_extractor_In_breast.py**  

Este script genera las carpetas y subcarpetas necesarias para organizar los datos. Se recomienda ejecutarlo primero con el dataset más pequeño, ya que los otros datasets son bastante extensos y, si ocurre algún error, tardaría mucho tiempo en detectarse.  

Después se pueden ejecutar los otros dos scripts:  

- **Conversor_extractor_CBIS.py**  
- **Conversor_extractor_DrMammo.py**  

Estos scripts no almacenan las imágenes directamente en la carpeta del dataset unificado; las guardan en subcarpetas separadas con la misma estructura. Esto evita sobrescribir imágenes existentes. Una vez convertidas, las imágenes se pueden mover a las carpetas correspondientes dentro del dataset unificado.

Una vez generadas las carpetas con los archivos TIFF para DrMammo y CBIS, se deben ejecutar los siguientes scripts:  

- **CBIS_a_Unificado.py**  
- **Mammo_a_Unificado.py**  

Estos scripts trasladan los datos de las subcarpetas al dataset unificado de manera ordenada, sin sobrescribir los archivos que ya existan.  

Es importante tener en cuenta que el proceso de conversión a TIFF puede ser bastante lento (varias horas) y requiere una cantidad considerable de memoria.

Al final del proceso se obtiene un dataset en el que las imágenes TIFF estarán organizadas en las carpetas correspondientes.  

Además, el siguiente script generará  CSV adicional que contiene un resumen de todos los datos, así como un EDA de los datos.

- **Ponderado_EDA.py**


## Licencia

Este trabajo y los scripts contenidos en este repositorio están bajo licencia:

**Creative Commons Attribution-NonCommercial 4.0 International (CC BY-NC 4.0)**  
[https://creativecommons.org/licenses/by-nc/4.0/](https://creativecommons.org/licenses/by-nc/4.0/)

Esto significa que:
- Se permite **copiar, redistribuir y adaptar** el contenido.  
- Se debe otorgar **crédito adecuado** al autor.  
- **No está permitido el uso comercial** del material.

