import wx
from stl import mesh
import pyvista as pv
import numpy as np
import pyperclip  # Necesario para copiar al portapapeles de manera sencilla (asegúrate de instalarlo)


class STLApp(wx.App):
    def OnInit(self):
        self.frame = wx.Frame(None, title="Reescalador STL Moderno", size=(600, 400))
        self.panel = wx.Panel(self.frame)
        self.panel.SetBackgroundColour("#F7F9FC")  # Fondo claro moderno

        # Título principal
        title = wx.StaticText(self.panel, label="Reescalador de Modelos 3D", pos=(20, 20))
        title_font = wx.Font(14, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_BOLD)
        title.SetFont(title_font)
        
        # Crear barra de menú
        menu_bar = wx.MenuBar()
    
        # Crear barra de menú
        menu_bar = wx.MenuBar()
        
        # Menú de ayuda
        menu_ayuda = wx.Menu()
        #item_ayuda = menu_ayuda.Append(wx.ID_HELP, "Ayuda")
        item_acerca = menu_ayuda.Append(wx.ID_ABOUT, "Acerca de")
        menu_bar.Append(menu_ayuda, "Ayuda")
        
        self.frame.SetMenuBar(menu_bar)
        
        # Asignar eventos
        #self.frame.Bind(wx.EVT_MENU, self.mostrar_acerca, item_ayuda)
        self.frame.Bind(wx.EVT_MENU, self.mostrar_acerca, item_acerca)
        
        # Botón para seleccionar archivo STL
        wx.StaticText(self.panel, label="Selecciona un archivo STL:", pos=(20, 80))
        select_btn = wx.Button(self.panel, label="Seleccionar", pos=(220, 75), size=(150, 30))
        select_btn.SetBackgroundColour("#0078D7")  # Azul estilo Windows
        select_btn.SetForegroundColour("white")
        select_btn.Bind(wx.EVT_BUTTON, self.seleccionar_archivo)

        self.file_path_label = wx.StaticText(self.panel, label="Ruta: Ningún archivo seleccionado", pos=(20, 120))
        self.file_path_label.Wrap(540)

        # Entrada para el factor de escala
        wx.StaticText(self.panel, label="Factor de escala:", pos=(20, 180))
        self.scale_input = wx.TextCtrl(self.panel, pos=(220, 175), size=(150, -1))
        self.scale_input.SetHint("Ejemplo: 1.5")

        # Botón para aplicar escala
        scale_btn = wx.Button(self.panel, label="Aplicar Escala", pos=(400, 175), size=(150, 30))
        scale_btn.SetBackgroundColour("#28A745")  # Verde
        scale_btn.SetForegroundColour("white")
        scale_btn.Bind(wx.EVT_BUTTON, self.aplicar_escala)

        # Botón para visualizar modelo
        visualize_btn = wx.Button(self.panel, label="Visualizar Modelo", pos=(220, 225), size=(150, 30))
        visualize_btn.SetBackgroundColour("#FFC107")  # Amarillo
        visualize_btn.SetForegroundColour("black")
        visualize_btn.Bind(wx.EVT_BUTTON, self.visualizar_archivo)

        # Botón para guardar como copia
        save_btn = wx.Button(self.panel, label="Guardar Modelo", pos=(400, 225), size=(150, 30))
        save_btn.SetBackgroundColour("#6C757D")  # Gris moderno
        save_btn.SetForegroundColour("white")
        save_btn.Bind(wx.EVT_BUTTON, self.guardar_archivo)
        
        
        
        # Checkbox para activar/desactivar la transparencia
        self.transparent_checkbox = wx.CheckBox(self.panel, label="Mostrar Transparencias", pos=(20, 260))
        self.transparent_checkbox.Bind(wx.EVT_CHECKBOX, self.toggle_transparency)
        
        
        self.frame.Show()
        return True
        
        

    def mostrar_acerca(self, event):
        """
        Muestra información sobre el programa y copia el correo al portapapeles.
        """
        correo = "excalibur_965@hotmail.com"
        mensaje_acerca = (
            "Reescalador STL\n\n"
            "Versión: 1.0.1\n"
            "Desarrollado por: Nahum Flores\n\n"
            "Este programa permite trabajar con archivos STL, ofreciendo herramientas "
            "para reescalar, visualizar y guardar modelos 3D. \nDiseñado con wxPython "
            "y PyVista.\n"
            f"Correo del desarrollador: {correo}\n\n"
            "Nota: El correo se ha copiado automáticamente al portapapeles."
        )
        
        # Copiar el correo al portapapeles
        try:
            pyperclip.copy(correo)
            aviso = "El correo del desarrollador ha sido copiado al portapapeles."
        except Exception as e:
            aviso = f"No se pudo copiar el correo al portapapeles: {e}"
        
        # Mostrar el mensaje "Acerca de" con la nota
        wx.MessageBox(mensaje_acerca, "Acerca de", wx.OK | wx.ICON_INFORMATION)
        wx.MessageBox(aviso, "Información", wx.OK | wx.ICON_INFORMATION)
        
    
    def toggle_transparency(self, event):
        """
        Activa o desactiva la transparencia para el modelo.
        """
        self.transparent = self.transparent_checkbox.IsChecked()
        
    def seleccionar_archivo(self, event):
        """Permite seleccionar un archivo STL."""
        with wx.FileDialog(self.frame, "Seleccionar archivo STL", wildcard="Archivos STL (*.stl)|*.stl") as dlg:
            if dlg.ShowModal() == wx.ID_OK:
                self.file_path = dlg.GetPath()
                self.modelo = mesh.Mesh.from_file(self.file_path)
                self.file_path_label.SetLabel(f"Ruta: {self.file_path}")
            else:
                wx.MessageBox("No se seleccionó ningún archivo.", "Información", wx.OK | wx.ICON_INFORMATION)

    def aplicar_escala(self, event):
        """Aplica un factor de escala al modelo cargado."""
        if not hasattr(self, 'modelo'):
            wx.MessageBox("Por favor, selecciona un archivo STL primero.", "Error", wx.OK | wx.ICON_ERROR)
            return

        try:
            factor_escala = float(self.scale_input.GetValue())
            if factor_escala <= 0:
                raise ValueError("El factor debe ser mayor a 0.")
            self.modelo.points *= factor_escala
            wx.MessageBox(f"Reescalado exitoso por un factor de {factor_escala}.", "Éxito", wx.OK | wx.ICON_INFORMATION)
        except ValueError:
            wx.MessageBox("Introduce un número válido para el factor de escala.", "Error", wx.OK | wx.ICON_ERROR)

    def calcular_volumen(self, modelo):
        """Calcula el volumen del modelo STL."""
        volumen = 0.0
        for vector in modelo.vectors:
            volumen += np.dot(vector[0], np.cross(vector[1], vector[2])) / 6.0
        return abs(volumen)

    def calcular_area_total(self, modelo):
        """Calcula el área total de la superficie del modelo STL."""
        area_total = 0.0
        for vector in modelo.vectors:
            lado1 = vector[1] - vector[0]
            lado2 = vector[2] - vector[0]
            area_total += np.linalg.norm(np.cross(lado1, lado2)) / 2.0
        return area_total

    def guardar_archivo(self, event):
        """Guarda el modelo STL modificado como copia."""
        if not hasattr(self, 'modelo'):
            wx.MessageBox("Por favor, selecciona un archivo STL primero y aplique cambios antes de guardar.", "Error", wx.OK | wx.ICON_ERROR)
            return

        try:
            nombre_original = self.file_path.split('/')[-1].split('.')[0]
            nombre_sugerido = f"{nombre_original}_modificado.stl"
            with wx.FileDialog(self.frame, "Guardar modelo STL como copia", defaultFile=nombre_sugerido, wildcard="Archivos STL (*.stl)|*.stl", style=wx.FD_SAVE | wx.FD_OVERWRITE_PROMPT) as dlg:
                if dlg.ShowModal() == wx.ID_OK:
                    ruta_guardado = dlg.GetPath()
                    self.modelo.save(ruta_guardado)
                    wx.MessageBox(f"Archivo guardado exitosamente como copia en:\n{ruta_guardado}", "Éxito", wx.OK | wx.ICON_INFORMATION)
                else:
                    wx.MessageBox("El archivo no fue guardado.", "Información", wx.OK | wx.ICON_INFORMATION)
        except Exception as e:
            wx.MessageBox(f"Error al guardar el archivo: {e}", "Error", wx.OK | wx.ICON_ERROR)

    def visualizar_archivo(self, event):
        """Representa el modelo STL en 3D con PyVista, mostrando información completa del objeto y reflejando cambios."""
        if not hasattr(self, 'modelo'):
            wx.MessageBox("Por favor, selecciona un archivo STL primero.", "Error", wx.OK | wx.ICON_ERROR)
            return
    
        try:
            volumen = self.calcular_volumen(self.modelo)
            area_total = self.calcular_area_total(self.modelo)
            num_triangles = self.modelo.vectors.shape[0]
    
            x_min, x_max = self.modelo.x.min(), self.modelo.x.max()
            y_min, y_max = self.modelo.y.min(), self.modelo.y.max()
            z_min, z_max = self.modelo.z.min(), self.modelo.z.max()
    
            ancho = x_max - x_min
            alto = y_max - y_min
            profundidad = z_max - z_min
    
            points = self.modelo.points.reshape(-1, 3)
            faces = []
            for i in range(len(self.modelo.vectors)):
                faces.extend([3, i * 3, i * 3 + 1, i * 3 + 2])
            faces = np.array(faces)
    
            num_vertices = len(points)
    
            mesh_data = pv.PolyData(points, faces)
            plotter = pv.Plotter()
            plotter.set_background("#333333")
    
            # Definir opacidad según el estado del checkbox
            is_transparent = hasattr(self, 'transparent') and self.transparent
            opacity_value = 0.5 if is_transparent else 1.0
    
            plotter.add_mesh(mesh_data, color="green", opacity=opacity_value, show_edges=True)
            plotter.add_axes()
            plotter.add_floor("z")
    
            light = pv.Light(position=(5, 5, 5), focal_point=(0, 0, 0), intensity=1.5)
            plotter.add_light(light)
    
            info_panel = (
                f"📂 Información del modelo:\n"
                f"  - Dimensiones (mm):\n"
                f"    • Ancho: {ancho:.2f} mm\n"
                f"    • Alto: {alto:.2f} mm\n"
                f"    • Profundidad: {profundidad:.2f} mm\n\n"
                f"  - Dimensiones (cm):\n"
                f"    • Ancho: {ancho / 10:.2f} cm\n"
                f"    • Alto: {alto / 10:.2f} cm\n"
                f"    • Profundidad: {profundidad / 10:.2f} cm\n\n"
                f"📏 Longitudes Totales:\n"
                f"    • Eje X: {x_max - x_min:.2f} mm / {(x_max - x_min) / 10:.2f} cm\n"
                f"    • Eje Y: {y_max - y_min:.2f} mm / {(y_max - y_min) / 10:.2f} cm\n"
                f"    • Eje Z: {z_max - z_min:.2f} mm / {(z_max - z_min) / 10:.2f} cm\n\n"
                f"📦 Volumen: {volumen:.2f} mm³ / {volumen / 1000:.2f} cm³\n"
                f"🖋️ Área Total: {area_total:.2f} mm² / {area_total / 100:.2f} cm²\n"
                f"🔺 Triángulos: {num_triangles}\n"
                f"🔷 Vértices: {num_vertices}\n"
            )
            plotter.add_text(info_panel, position="upper_left", font_size=10)
    
            def reset_camera():
                plotter.camera_position = "iso"
    
            plotter.add_key_event("r", reset_camera)
            plotter.add_key_event("+", lambda: plotter.camera.zoom(1.2))
            plotter.add_key_event("-", lambda: plotter.camera.zoom(0.8))
            plotter.show()
    
        except Exception as e:
            wx.MessageBox(f"Error al visualizar el archivo: {e}", "Error", wx.OK | wx.ICON_ERROR)


if __name__ == "__main__":
    app = STLApp()  # Crear instancia de la aplicación
    app.MainLoop()  # Iniciar el ciclo de eventos de wxPython