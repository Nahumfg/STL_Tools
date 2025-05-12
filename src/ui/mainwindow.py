#!/usr/bin/env python3
"""
Módulo: mainwindow.py

Esta interfaz gráfica (usando wxPython) permite:
  - Seleccionar y cargar archivos STL.
  - Aplicar un factor de escala al modelo STL.
  - Exportar (guardar) el modelo escalado.
  - Importar escalas estándar desde un archivo Excel.
  
Integra los módulos de negocio previamente desarrollados:
    - stl_reader.py
    - stl_scaler.py
    - stl_export.py
    - excel_importer.py
    - scale_db.py (opcional en este flujo)
"""

import wx
import os
from pathlib import Path

# Importamos los módulos de negocio
# En src/ui/mainwindow.py
from stl_reader import STLReader
from stl_scaler import scale_model
from stl_export import export_mesh
from excel_importer import import_scales_from_excel
# La importación se realiza de manera local al evento, para evitar dependencias circulares si se requiere.
# from excel_importer import import_scales_from_excel

class MainWindow(wx.Frame):
    def __init__(self, parent, title="Reescalador STL Moderno", size=(800, 600)):
        super(MainWindow, self).__init__(parent, title=title, size=size)
        self.panel = wx.Panel(self)
        self.stl_model = None  # Aquí se almacenará el modelo STL (tipo mesh.Mesh)

        # Botón para seleccionar archivo STL
        self.btn_select = wx.Button(self.panel, label="Seleccionar archivo STL", pos=(20, 20))
        self.btn_select.Bind(wx.EVT_BUTTON, self.on_select_file)
        
        # Etiqueta para mostrar la ruta del archivo cargado
        self.txt_path = wx.StaticText(self.panel, label="Ningún archivo seleccionado", pos=(20, 60))
        
        # Campo y etiqueta para ingresar el factor de escala
        self.txt_factor_label = wx.StaticText(self.panel, label="Factor de escala:", pos=(20, 100))
        self.txt_factor = wx.TextCtrl(self.panel, pos=(150, 95), size=(100, -1))
        
        # Botón para aplicar el escalado
        self.btn_scale = wx.Button(self.panel, label="Aplicar escala", pos=(20, 140))
        self.btn_scale.Bind(wx.EVT_BUTTON, self.on_scale)
        
        # Botón para exportar (guardar) el modelo STL escalado
        self.btn_export = wx.Button(self.panel, label="Exportar modelo STL", pos=(150, 140))
        self.btn_export.Bind(wx.EVT_BUTTON, self.on_export)
        
        # Botón para importar escalas desde un archivo Excel
        self.btn_import_excel = wx.Button(self.panel, label="Importar escalas desde Excel", pos=(20, 180))
        self.btn_import_excel.Bind(wx.EVT_BUTTON, self.on_import_excel)
        
        # Menú (puedes ampliarlo con más opciones)
        menubar = wx.MenuBar()
        fileMenu = wx.Menu()
        # Aquí podrías agregar opciones adicionales al menú "Archivo"
        menubar.Append(fileMenu, "Archivo")
        self.SetMenuBar(menubar)
        
        self.Centre()
        self.Show()

    def on_select_file(self, event):
        """Permite seleccionar un archivo STL y cargar el modelo usando STLReader."""
        dlg = wx.FileDialog(self, "Seleccionar archivo STL", wildcard="STL files (*.stl)|*.stl", style=wx.FD_OPEN)
        if dlg.ShowModal() == wx.ID_OK:
            file_path = dlg.GetPath()
            self.txt_path.SetLabel(f"Archivo: {file_path}")
            try:
                reader = STLReader(file_path)
                self.stl_model = reader.read()  # Se espera recibir una instancia de mesh.Mesh
                wx.MessageBox("Modelo STL cargado correctamente.", "Éxito", wx.OK | wx.ICON_INFORMATION)
            except Exception as e:
                wx.MessageBox(f"Error al cargar el archivo STL:\n{e}", "Error", wx.OK | wx.ICON_ERROR)
        dlg.Destroy()

    def on_scale(self, event):
        """Aplica el factor de escala ingresado en el campo a la instancia del modelo STL."""
        if self.stl_model is None:
            wx.MessageBox("Primero carga un archivo STL.", "Error", wx.OK | wx.ICON_ERROR)
            return
        try:
            factor = float(self.txt_factor.GetValue())
            # Se aplica el escalado in situ. Puedes optar por inplace=False para crear una copia.
            self.stl_model = scale_model(self.stl_model, factor, inplace=True)
            wx.MessageBox(f"Modelo escalado con factor {factor}.", "Éxito", wx.OK | wx.ICON_INFORMATION)
        except ValueError:
            wx.MessageBox("Ingresa un valor numérico válido para el factor.", "Error", wx.OK | wx.ICON_ERROR)

    def on_export(self, event):
        """Permite exportar (guardar) el modelo STL actualmente cargado, en formato binario."""
        if self.stl_model is None:
            wx.MessageBox("Carga un archivo STL y aplica escala antes de exportar.", "Error", wx.OK | wx.ICON_ERROR)
            return
        dlg = wx.FileDialog(self, "Guardar archivo STL", wildcard="STL files (*.stl)|*.stl",
                            style=wx.FD_SAVE | wx.FD_OVERWRITE_PROMPT)
        if dlg.ShowModal() == wx.ID_OK:
            export_path = dlg.GetPath()
            try:
                export_mesh(self.stl_model, export_path, binary=True)
                wx.MessageBox("Modelo exportado correctamente.", "Éxito", wx.OK | wx.ICON_INFORMATION)
            except Exception as e:
                wx.MessageBox(f"Error al exportar el modelo:\n{e}", "Error", wx.OK | wx.ICON_ERROR)
        dlg.Destroy()

    def on_import_excel(self, event):
        """Permite importar escalas desde un archivo Excel y cargarlas en la base de datos."""
        dlg = wx.FileDialog(self, "Seleccionar archivo Excel", wildcard="Excel files (*.xlsx)|*.xlsx",
                            style=wx.FD_OPEN)
        if dlg.ShowModal() == wx.ID_OK:
            excel_path = dlg.GetPath()
            try:
                # Se importa la función recién creada en el módulo excel_importer
                from excel_importer import import_scales_from_excel
                import_scales_from_excel(excel_path)
                wx.MessageBox("Escalas importadas desde Excel correctamente.", "Éxito", wx.OK | wx.ICON_INFORMATION)
            except Exception as e:
                wx.MessageBox(f"Error al importar escalas:\n{e}", "Error", wx.OK | wx.ICON_ERROR)
        dlg.Destroy()

if __name__ == '__main__':
    app = wx.App(False)
    MainWindow(None)
    app.MainLoop()