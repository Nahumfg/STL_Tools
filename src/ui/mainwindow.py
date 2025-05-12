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
import wx.lib.agw.aui as aui
import os
from pathlib import Path

# Importamos los módulos de negocio
from stl_reader import STLReader
from stl_scaler import scale_model
from stl_export import export_mesh
from excel_importer import import_scales_from_excel


class MainWindow(wx.Frame):
    def __init__(self, parent, title="Reescalador STL", size=(800, 600)):
        super(MainWindow, self).__init__(parent, title=title, size=size)
        
        # Configuramos el AUI Manager para un layout versátil
        self.aui_manager = aui.AuiManager(self)
        
        # Panel principal con fondo neutro
        self.main_panel = wx.Panel(self)
        self.main_panel.SetBackgroundColour(wx.Colour(245, 245, 245))
        
        # Creamos el sizer principal (layout vertical)
        main_sizer = wx.BoxSizer(wx.VERTICAL)
        
        # Título de la ventana
        title_text = wx.StaticText(self.main_panel, label="Reescalador STL")
        title_font = wx.Font(14, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_BOLD)
        title_text.SetFont(title_font)
        title_text.SetForegroundColour(wx.Colour(52, 73, 94))
        main_sizer.Add(title_text, 0, wx.ALL | wx.ALIGN_CENTER_HORIZONTAL, 10)
        
        # Sizer para seleccionar el archivo STL
        file_sizer = wx.BoxSizer(wx.HORIZONTAL)
        self.btn_select = wx.Button(self.main_panel, label="Seleccionar archivo STL")
        self.btn_select.SetBackgroundColour(wx.Colour(52, 152, 219))
        self.btn_select.SetForegroundColour(wx.Colour(255, 255, 255))
        file_sizer.Add(self.btn_select, 0, wx.ALL, 5)
        self.txt_path = wx.StaticText(self.main_panel, label="Ningún archivo seleccionado")
        file_sizer.Add(self.txt_path, 1, wx.ALL | wx.ALIGN_CENTER_VERTICAL, 5)
        main_sizer.Add(file_sizer, 0, wx.EXPAND | wx.LEFT | wx.RIGHT, 10)
        
        # Sizer para ingresar el factor de escala
        factor_sizer = wx.BoxSizer(wx.HORIZONTAL)
        self.txt_factor_label = wx.StaticText(self.main_panel, label="Factor de escala:")
        factor_sizer.Add(self.txt_factor_label, 0, wx.ALL | wx.ALIGN_CENTER_VERTICAL, 5)
        self.txt_factor = wx.TextCtrl(self.main_panel)
        factor_sizer.Add(self.txt_factor, 0, wx.ALL, 5)
        main_sizer.Add(factor_sizer, 0, wx.LEFT | wx.RIGHT, 10)
        
        # Sizer para los botones de acción
        action_sizer = wx.BoxSizer(wx.HORIZONTAL)
        self.btn_scale = wx.Button(self.main_panel, label="Aplicar escala")
        self.btn_scale.SetBackgroundColour(wx.Colour(46, 204, 113))
        self.btn_scale.SetForegroundColour(wx.Colour(255, 255, 255))
        action_sizer.Add(self.btn_scale, 0, wx.ALL, 5)
        self.btn_export = wx.Button(self.main_panel, label="Exportar modelo STL")
        self.btn_export.SetBackgroundColour(wx.Colour(41, 128, 185))
        self.btn_export.SetForegroundColour(wx.Colour(255, 255, 255))
        action_sizer.Add(self.btn_export, 0, wx.ALL, 5)
        self.btn_import_excel = wx.Button(self.main_panel, label="Importar escalas desde Excel")
        self.btn_import_excel.SetBackgroundColour(wx.Colour(155, 89, 182))
        self.btn_import_excel.SetForegroundColour(wx.Colour(255, 255, 255))
        action_sizer.Add(self.btn_import_excel, 0, wx.ALL, 5)
        main_sizer.Add(action_sizer, 0, wx.ALIGN_CENTER_HORIZONTAL)
        
        # Asignar el sizer al panel principal
        self.main_panel.SetSizer(main_sizer)
        
        # Agregar el panel principal al AUI Manager y actualizar
        self.aui_manager.AddPane(self.main_panel, aui.AuiPaneInfo().CenterPane().Name("MainPanel"))
        self.aui_manager.Update()        
        
        # Bind para los eventos de los botones
        self.btn_select.Bind(wx.EVT_BUTTON, self.on_select_file)
        self.btn_scale.Bind(wx.EVT_BUTTON, self.on_scale)
        self.btn_export.Bind(wx.EVT_BUTTON, self.on_export)
        self.btn_import_excel.Bind(wx.EVT_BUTTON, self.on_import_excel)
        
        self.stl_model = None  # Aquí se almacenará el modelo STL (tipo mesh.Mesh)
        
        # Menú simple (puedes agregar más opciones)
        menubar = wx.MenuBar()
        file_menu = wx.Menu()
        menubar.Append(file_menu, "Archivo")
        self.SetMenuBar(menubar)
        
        self.Center()
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
        """Aplica el factor de escala ingresado al modelo STL cargado."""
        if self.stl_model is None:
            wx.MessageBox("Primero carga un archivo STL.", "Error", wx.OK | wx.ICON_ERROR)
            return
        try:
            factor = float(self.txt_factor.GetValue())
            self.stl_model = scale_model(self.stl_model, factor, inplace=True)
            wx.MessageBox(f"Modelo escalado con factor {factor}.", "Éxito", wx.OK | wx.ICON_INFORMATION)
        except ValueError:
            wx.MessageBox("Ingresa un valor numérico válido para el factor.", "Error", wx.OK | wx.ICON_ERROR)

    def on_export(self, event):
        """Exporta el modelo STL escalado en formato binario."""
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
        """Importa escalas desde un archivo Excel y las inserta en la base de datos."""
        dlg = wx.FileDialog(self, "Seleccionar archivo Excel", wildcard="Excel files (*.xlsx)|*.xlsx",
                            style=wx.FD_OPEN)
        if dlg.ShowModal() == wx.ID_OK:
            excel_path = dlg.GetPath()
            try:
                import_scales_from_excel(excel_path)
                wx.MessageBox("Escalas importadas desde Excel correctamente.", "Éxito", wx.OK | wx.ICON_INFORMATION)
            except Exception as e:
                wx.MessageBox(f"Error al importar escalas:\n{e}", "Error", wx.OK | wx.ICON_ERROR)
        dlg.Destroy()


if __name__ == '__main__':
    app = wx.App(False)
    MainWindow(None)
    app.MainLoop()