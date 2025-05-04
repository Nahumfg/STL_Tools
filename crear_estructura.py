import os
import tkinter as tk
from tkinter import filedialog

# Definir la estructura del proyecto
estructura = {
    "config": [],
    "excel_files": [],
    "logs": [],
    "src": ["main.py", "requirements.txt"],
    "src/modules": ["stl_reader.py", "stl_scaler.py", "stl_export.py", "utils.py"],
    "src/ui": ["mainwindow.py"],
}

def crear_estructura(base_path):
    for carpeta, archivos in estructura.items():
        carpeta_path = os.path.join(base_path, carpeta)
        os.makedirs(carpeta_path, exist_ok=True)  # Crea la carpeta si no existe

        for archivo in archivos:
            archivo_path = os.path.join(carpeta_path, archivo)
            if not os.path.exists(archivo_path):  # Solo crea archivos si no existen
                with open(archivo_path, 'w') as f:
                    f.write("")  # Archivo vacío

def seleccionar_carpeta_y_crear():
    root = tk.Tk()
    root.withdraw()  # Ocultar ventana principal
    carpeta_seleccionada = filedialog.askdirectory(title="Selecciona la carpeta base del proyecto")
    
    if carpeta_seleccionada:
        crear_estructura(carpeta_seleccionada)
        print(f"Estructura creada o modificada en: {carpeta_seleccionada}")
    else:
        print("No se seleccionó ninguna carpeta.")

if __name__ == "__main__":
    seleccionar_carpeta_y_crear()