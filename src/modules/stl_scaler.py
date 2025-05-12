#!/usr/bin/env python3
"""
Módulo: stl_scaler.py

Este módulo proporciona la funcionalidad para escalar un modelo STL mediante un factor dado.
Utiliza la biblioteca numpy-stl para manipular el objeto del modelo STL (mesh.Mesh) de forma uniforme.

Mejoras:
  - Verificación del tipo de modelo para asegurarnos de que se trata de una instancia de mesh.Mesh.
  - Validación del factor de escala.
  - Actualización de las normales (si el objeto posee el método update_normals) tras modificar las coordenadas.
  - Posibilidad de trabajar en modo inplace o creando una copia.
  
El objetivo es facilitar la conversión de escalas (por ejemplo, de 1:1 a 1:36) de manera segura.
"""

from stl import mesh

def scale_model(stl_model: mesh.Mesh, factor: float, inplace: bool = True) -> mesh.Mesh:
    """
    Escala un modelo STL por el factor indicado de manera uniforme.

    Args:
        stl_model (mesh.Mesh): Modelo STL a escalar.
        factor (float): Factor de escala (debe ser un número > 0).
        inplace (bool, opcional): Si True, modifica el modelo original.
                                  Si False, retorna una copia escalada. Por defecto es True.

    Returns:
        mesh.Mesh: El modelo escalado.

    Raises:
        TypeError: Si el modelo no es una instancia de mesh.Mesh o si el factor no es numérico.
        ValueError: Si el factor es menor o igual a 0.
    """
    # Verificamos que el factor es numérico
    if not isinstance(factor, (int, float)):
        raise TypeError("El factor de escala debe ser un número.")
    if factor <= 0:
        raise ValueError("El factor de escala debe ser mayor que cero.")
    
    # Verificamos que se trata de un objeto mesh.Mesh
    if not isinstance(stl_model, mesh.Mesh):
        raise TypeError("El modelo STL debe ser una instancia de mesh.Mesh.")

    if inplace:
        stl_model.vectors *= factor
        # Si el objeto dispone de update_normals, se actualizan para mantener la coherencia.
        if hasattr(stl_model, "update_normals"):
            stl_model.update_normals()
        return stl_model
    else:
        # Se crea una copia del modelo (asegurándonos de copiar los datos)
        new_model = mesh.Mesh(stl_model.data.copy())
        new_model.vectors *= factor
        if hasattr(new_model, "update_normals"):
            new_model.update_normals()
        return new_model

# Para casos específicos, se podría ampliar la funcionalidad y permitir escalado no uniforme.
# Por ejemplo, si en el futuro se desea aplicar factores distintos para X, Y y Z,
# se podría extender este método o crear una nueva función que acepte un tuple (factor_x, factor_y, factor_z).