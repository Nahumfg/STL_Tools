#!/usr/bin/env python3
import struct
from pathlib import Path
from typing import Any, Dict, List, Tuple

class STLReader:
    """
    Clase para leer archivos STL en formato ASCII y binario.
    
    Provee el método `read()` para la detección y parseo.
    Los datos se retornan en un diccionario con, al menos, la clave
    'facets', que contiene una lista de diccionarios con keys 'normal'
    y 'vertices'.
    """

    def __init__(self, file_path: str) -> None:
        """
        Inicializa el lector con la ruta del archivo STL.
        """
        self.file_path = Path(file_path).resolve()

    def read(self) -> Dict[str, Any]:
        """
        Lee el archivo STL y retorna un diccionario con los datos del modelo.

        Utiliza heurísticas basadas en el tamaño del archivo y el encabezado
        para distinguir entre formato binario y ASCII.

        Returns:
            dict: {
                'header': <str> (solo para binario),
                'facets': [ { 'normal': tuple, 'vertices': [tuple, ...] }, ... ]
            }

        Raises:
            FileNotFoundError: Si el archivo no existe.
            Exception: Para errores durante la lectura.
        """
        if not self.file_path.exists():
            raise FileNotFoundError(f"El archivo '{self.file_path}' no existe.")

        file_size = self.file_path.stat().st_size

        # Abrir en modo binario para leer el encabezado y detectar formato
        with self.file_path.open("rb") as f:
            header = f.read(80)
            triangle_count_bytes = f.read(4)
            # Si se pudieron leer 4 bytes para el contador, probamos interpretar el número de facetas
            if len(triangle_count_bytes) == 4:
                triangle_count = struct.unpack("<I", triangle_count_bytes)[0]
                expected_binary_size = 84 + (triangle_count * 50)
                # Si el tamaño esperado coincide con el tamaño del archivo,
                # se asume que es un STL binario
                if expected_binary_size == file_size:
                    return self._read_binary(f, header, triangle_count)
        # En caso contrario, asumimos que es un STL ASCII
        return self._read_ascii()

    def _read_binary(self, file_obj, header: bytes, triangle_count: int) -> Dict[str, Any]:
        """
        Procesa el archivo STL en formato binario.

        Args:
            file_obj: Objeto de archivo abierto en modo binario, posicionado tras leer el contador.
            header (bytes): Encabezado de 80 bytes.
            triangle_count (int): Número de facetas indicadas en el archivo.

        Returns:
            dict: Diccionario con el encabezado (como string) y la lista de facetas.
        """
        facets: List[Dict[str, Any]] = []
        for i in range(triangle_count):
            # Cada faceta ocupa 50 bytes:
            #  • 48 bytes para 12 floats (1 normal y 3 vértices)
            #  •  2 bytes para atributos (se ignoran)
            facet_data = file_obj.read(50)
            if len(facet_data) != 50:
                raise ValueError(f"Datos incompletos en la faceta número {i}.")
            # Desempaquetar 12 floats (cada uno de 4 bytes)
            numbers = struct.unpack("<12f", facet_data[:48])
            normal = numbers[0:3]
            # Agrupar los vértices (cada uno de 3 floats)
            vertices = [numbers[3:6], numbers[6:9], numbers[9:12]]
            facets.append({
                "normal": normal,
                "vertices": vertices
            })

        # Convertir el encabezado a string (puede incluir un identificador o nombre)
        header_str = header.decode("utf-8", errors="ignore").strip()
        return {"header": header_str, "facets": facets}

    def _read_ascii(self) -> Dict[str, Any]:
        """
        Procesa el archivo STL en formato ASCII.

        Lee el archivo en modo texto y extrae cada faceta buscando las líneas
        que contienen 'facet normal' y 'vertex'. Se asume que el archivo sigue
        el formato estándar de STL ASCII.

        Returns:
            dict: Diccionario con la lista de facetas.
        """
        facets: List[Dict[str, Any]] = []
        try:
            with self.file_path.open("r", encoding="utf-8", errors="ignore") as f:
                lines = [line.strip() for line in f if line.strip()]
        except Exception as e:
            raise Exception(f"Error al leer el archivo en modo ASCII: {e}")

        i = 0
        while i < len(lines):
            line_lower = lines[i].lower()
            if line_lower.startswith("facet normal"):
                parts = lines[i].split()
                try:
                    # Se espera que los últimos tres elementos sean las componentes del vector normal
                    normal = tuple(map(float, parts[-3:]))
                except ValueError:
                    normal = (0.0, 0.0, 0.0)
                i += 1  # Avanzar a la siguiente línea, que idealmente es "outer loop"

                if i < len(lines) and lines[i].lower() == "outer loop":
                    i += 1  # Saltar la línea "outer loop"

                vertices: List[Tuple[float, float, float]] = []
                # Leer las tres líneas que definen los vértices
                for _ in range(3):
                    if i < len(lines) and lines[i].lower().startswith("vertex"):
                        try:
                            vertex_parts = lines[i].split()
                            vertex = tuple(map(float, vertex_parts[-3:]))
                        except ValueError:
                            vertex = (0.0, 0.0, 0.0)
                        vertices.append(vertex)
                        i += 1
                    else:
                        break

                # Saltar líneas hasta encontrar "endfacet"
                while i < len(lines) and not lines[i].lower().startswith("endfacet"):
                    i += 1
                facets.append({"normal": normal, "vertices": vertices})
            else:
                i += 1

        return {"facets": facets}

# Ejemplo de uso:
if __name__ == "__main__":
    # Actualiza 'ruta_al_archivo.stl' con la ruta real de tu archivo STL.
    stl_file = "ruta_al_archivo.stl"
    reader = STLReader(stl_file)
    try:
        model = reader.read()
        facets = model.get("facets", [])
        print("Número de facetas leídas:", len(facets))
    except Exception as e:
        print("Error al leer el archivo STL:", e)