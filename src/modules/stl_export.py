#!/usr/bin/env python3
"""
Módulo: stl_export.py

Este módulo proporciona una función para exportar (guardar)
un objeto STL (instancia de mesh.Mesh de la biblioteca numpy-stl)
a un archivo en disco. Se puede elegir entre guardar en formato binario o ASCII.
"""

from pathlib import Path
from stl import mesh  # Asegúrate de tener instalada la biblioteca numpy-stl.
from typing import Union

# Opcional: Si deseas dar la opción de elegir entre ASCII o binario,
# puedes importar el enumerado Mode (si está disponible en tu versión).
# from stl import Mode

def export_mesh(
    stl_model: mesh.Mesh,
    file_path: Union[str, Path],
    binary: bool = True
) -> None:
    """
    Exporta un modelo STL a un archivo en disco.

    Args:
        stl_model (mesh.Mesh): Instancia del modelo STL que se desea exportar.
        file_path (Union[str, Path]): Ruta del archivo de destino. Debe tener extensión .stl.
        binary (bool, optional): Indica si se debe guardar en formato binario (True) o ASCII (False).
                                   Por defecto es True (binario).

    Raises:
        ValueError: Si el archivo de destino no tiene extensión .stl.
        Exception: Para errores generales durante la exportación.
    """
    target_path = Path(file_path).resolve()
    
    # Validar que el archivo tenga extensión .stl
    if target_path.suffix.lower() != ".stl":
        raise ValueError("El archivo de destino debe tener extensión .stl")
    
    try:
        # Si la biblioteca soporta un parámetro para elegir entre binario/ASCII,
        # se puede hacer algo similar a lo siguiente.
        #
        # from stl import Mode
        # mode = Mode.BINARY if binary else Mode.ASCII
        # stl_model.save(str(target_path), mode=mode)
        #
        # Como opción por defecto, se utiliza el método save() tal y como lo ofrece
        # numpy-stl, que guarda en binario por defecto.
        if binary:
            stl_model.save(str(target_path))
        else:
            # Muchos modelos permiten guardar en ASCII marcando mode="ascii"
            # dependiendo de la versión de numpy-stl. Si no, se puede utilizar
            # un método específico (ver documentación de la librería).
            stl_model.save(str(target_path), mode=stl.MODE_ASCII)
    except Exception as e:
        raise Exception(f"Error al exportar el archivo STL: {e}")

# Ejemplo de uso:
if __name__ == "__main__":
    # Para efectos de demostración se crea un modelo STL ficticio de un único triángulo.
    import numpy as np
    
    # Se crea un arreglo vacío con el dtype esperado:
    data = np.zeros(1, dtype=mesh.Mesh.dtype)
    test_model = mesh.Mesh(data)
    
    # Asignar manualmente algunos valores a 'points'.
    test_model.points = np.array([
        [0.0, 0.0, 0.0],
        [1.0, 0.0, 0.0],
        [0.0, 1.0, 0.0]
    ])
    
    # Intentar exportar el modelo.
    try:
        export_path = "modelo_exportado.stl"  # Asegúrate de tener permisos para escribir en la carpeta.
        export_mesh(test_model, export_path, binary=True)
        print(f"El modelo STL se ha exportado exitosamente en: {export_path}")
    except Exception as err:
        print("Error al exportar el modelo:", err)