#!/usr/bin/env python3
"""
Archivo: main.py
Punto de entrada para la aplicación STL_Tools. 
Este script prepara el entorno añadiendo la carpeta "src" al sys.path y lanza la interfaz gráfica.
"""

import sys
from pathlib import Path

# Agregamos la carpeta "src" al sys.path para que se puedan importar los módulos y la UI correctamente.
src_path = Path(__file__).resolve().parent / "src"
if str(src_path) not in sys.path:
    sys.path.append(str(src_path))

# Ahora, como "src" está en el path, importamos la interfaz gráfica.
from ui.mainwindow import MainWindow
import wx

def main():
    # Creamos la aplicación wxPython y mostramos la ventana principal.
    app = wx.App(False)
    frame = MainWindow(None)
    frame.Show()  # La ventana se muestra; en mainwindow.py ya se llama a Centre() y Show(), pero esta línea es opcional.
    app.MainLoop()

if __name__ == '__main__':
    main()