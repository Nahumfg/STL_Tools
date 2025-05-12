#!/usr/bin/env python3
"""
Módulo: excel_importer.py

Este módulo proporciona funciones para importar registros de escalas estándar
desde archivos Excel ubicados en la carpeta "Excel_files" y cargarlos en la 
base de datos mediante el módulo scale_db.
"""

import os
from pathlib import Path
from typing import Optional

import pandas as pd

# Importamos la clase ScaleDB que maneja la base de datos.
# Como scale_db.py se encuentra en el mismo directorio que excel_importer.py,
# usamos una importación directa.
from scale_db import ScaleDB


def import_scales_from_excel(file_path: str) -> None:
    """
    Importa registros de escalas desde un archivo Excel a la base de datos.

    El archivo debe contener las siguientes columnas:
      - object_name: nombre del objeto o modelo.
      - original_scale: escala original (por ejemplo, "1:1").
      - desired_scale: escala deseada (por ejemplo, "1:36").
      - conversion_factor: factor de conversión numérico (ejemplo, 0.0278 para 1:36).
      - notes: notas adicionales (opcional).

    Args:
        file_path (str): Ruta del archivo Excel a importar.
    
    Raises:
        FileNotFoundError: Si el archivo Excel no se encuentra.
        ValueError: Si el Excel no contiene las columnas requeridas.
        Exception: Para errores en la lectura del archivo.
    """
    excel_file = Path(file_path)
    if not excel_file.exists():
        raise FileNotFoundError(f"El archivo Excel '{file_path}' no existe.")

    try:
        # Leer el archivo Excel. Se recomienda que la codificación y el motor sean adecuados.
        df = pd.read_excel(file_path)
    except Exception as e:
        raise Exception(f"Error al leer el archivo Excel: {e}")
    
    # Verificar que existen las columnas requeridas
    required_columns = ["object_name", "original_scale", "desired_scale", "conversion_factor"]
    missing_columns = [col for col in required_columns if col not in df.columns]
    if missing_columns:
        raise ValueError(f"Las siguientes columnas requeridas faltan en el Excel: {', '.join(missing_columns)}")

    # Crear una instancia de la base de datos
    db = ScaleDB()
    print("Iniciando la importación de registros desde Excel...")
    try:
        # Iteramos sobre cada fila del DataFrame y agregamos el registro a la base de datos.
        for index, row in df.iterrows():
            object_name: str = row["object_name"]
            original_scale: str = row["original_scale"]
            desired_scale: str = row["desired_scale"]
            conversion_factor: float = row["conversion_factor"]
            # La columna 'notes' es opcional
            notes: Optional[str] = row.get("notes") if "notes" in row.index else None

            # Insertar el registro en la base de datos utilizando el método add_scale
            record_id = db.add_scale(
                object_name=object_name,
                original_scale=original_scale,
                desired_scale=desired_scale,
                conversion_factor=conversion_factor,
                notes=notes
            )
            print(f"Registro importado con ID: {record_id}")
    finally:
        db.close()
    print("Importación completada exitosamente.")


if __name__ == "__main__":
    # Ejemplo de uso:
    # Se asume que en la carpeta 'Excel_files' existe un archivo llamado 'medidas.xlsx'
    excel_path = os.path.join("Excel_files", "medidas.xlsx")
    try:
        import_scales_from_excel(excel_path)
    except Exception as err:
        print("Error durante la importación de escalas desde Excel:", err)