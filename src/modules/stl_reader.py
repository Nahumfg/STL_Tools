import os
import struct

class STLReader:
    """
    Clase para leer archivos STL en formatos ASCII y binario.
    
    Provee el método `read()` para detección y parseo.
    Los datos se retornan en un diccionario con, al menos,
    una clave 'facets' que contiene una lista de diccionarios,
    cada uno con 'normal' y 'vertices'.
    """
    
    def __init__(self, file_path):
        """
        Inicializa el lector con la ruta del archivo STL.
        """
        self.file_path = file_path

    def read(self):
        """
        Lee el archivo STL y retorna un diccionario con los datos del modelo.
        
        Utiliza heurísticas basadas en el tamaño del archivo y el encabezado
        para distinguir entre formato binario y ASCII.
        
        Returns:
            dict: { 'header': <str> (solo para binario), 'facets': [ { 'normal': tuple, 'vertices': [tuple, ...] }, ... ] }
        
        Raises:
            FileNotFoundError: Si el archivo no existe.
            Exception: Para errores durante la lectura.
        """
        if not os.path.exists(self.file_path):
            raise FileNotFoundError(f"El archivo '{self.file_path}' no existe.")

        file_size = os.path.getsize(self.file_path)
        
        # Abrir en modo binario para leer encabezado y determinar el formato
        with open(self.file_path, 'rb') as f:
            header = f.read(80)
            triangle_count_bytes = f.read(4)
            # Si tenemos los 4 bytes siguientes, tratamos de interpretar el conteo de facetas
            if len(triangle_count_bytes) == 4:
                triangle_count = struct.unpack('<I', triangle_count_bytes)[0]
                expected_binary_size = 84 + (triangle_count * 50)
                # Si el tamaño esperado coincide, entonces es un archivo binario
                if expected_binary_size == file_size:
                    return self._read_binary(f, header, triangle_count)
        # Si no se cumplen las condiciones anteriores, asumimos que es ASCII.
        return self._read_ascii()

    def _read_binary(self, file_obj, header, triangle_count):
        """
        Procesa el archivo STL en formato binario.
        
        Args:
            file_obj: Objeto de archivo abierto en modo binario, posicionado tras leer el contador.
            header (bytes): Encabezado de 80 bytes.
            triangle_count (int): Número de facetas que se indican en el archivo.
            
        Returns:
            dict: Diccionario con el encabezado (como string) y la lista de facetas.
        """
        facets = []
        for i in range(triangle_count):
            # Cada faceta ocupa 50 bytes:
            # • 48 bytes (12 floats) para normal y tres vértices.
            # • 2 bytes adicionales para atributos.
            facet_data = file_obj.read(50)
            if len(facet_data) != 50:
                raise ValueError(f"Datos incompletos en la faceta número {i}.")
            # Desempaquétalo: '<12f' para los 12 números (4 bytes cada uno)
            numbers = struct.unpack('<12f', facet_data[:48])
            normal = numbers[0:3]
            # Agrupa los vértices: cada vértice se compone de 3 floats
            vertices = [numbers[3:6], numbers[6:9], numbers[9:12]]
            facets.append({
                'normal': normal,
                'vertices': vertices
            })
        # Decodificar el encabezado (puede incluir un identificador o nombre)
        header_str = header.decode('utf-8', errors='ignore').strip()
        return {'header': header_str, 'facets': facets}

    def _read_ascii(self):
        """
        Procesa el archivo STL en formato ASCII.
        
        Lee el archivo en modo texto y extrae cada faceta buscando las líneas
        que contienen 'facet normal' y 'vertex'. Se asume que el archivo sigue 
        el formato estándar de STL ASCII.
        
        Returns:
            dict: Diccionario con la lista de facetas.
        """
        facets = []
        try:
            with open(self.file_path, 'r', encoding='utf-8', errors='ignore') as f:
                # Leer líneas y eliminar espacios en blanco
                lines = [line.strip() for line in f if line.strip()]
        except Exception as e:
            raise Exception(f"Error al leer el archivo en modo ASCII: {e}")
        
        i = 0
        while i < len(lines):
            line_lower = lines[i].lower()
            if line_lower.startswith('facet normal'):
                parts = lines[i].split()
                try:
                    # Se asume que los últimos tres números son las componentes del vector normal
                    normal = tuple(map(float, parts[-3:]))
                except ValueError:
                    normal = (0.0, 0.0, 0.0)
                i += 1  # Pasar a la siguiente línea (se espera "outer loop")
                
                if i < len(lines) and lines[i].lower() == 'outer loop':
                    i += 1  # Saltar la línea "outer loop"
                
                vertices = []
                # Leer las tres líneas que contienen los vértices
                for _ in range(3):
                    if i < len(lines) and lines[i].lower().startswith('vertex'):
                        try:
                            vertex_parts = lines[i].split()
                            vertex = tuple(map(float, vertex_parts[-3:]))
                        except ValueError:
                            vertex = (0.0, 0.0, 0.0)
                        vertices.append(vertex)
                        i += 1
                    else:
                        break
                # Saltar hasta la línea que indique el fin de la faceta ("endfacet")
                while i < len(lines) and not lines[i].lower().startswith('endfacet'):
                    i += 1
                facets.append({'normal': normal, 'vertices': vertices})
            else:
                i += 1
        return {'facets': facets}


# Ejemplo de uso:
if __name__ == '__main__':
    # Cambia 'ruta_al_archivo.stl' por la ruta real de tu archivo STL
    stl_file = 'ruta_al_archivo.stl'
    reader = STLReader(stl_file)
    try:
        model = reader.read()
        facets = model.get('facets', [])
        print("Número de facetas leídas:", len(facets))
    except Exception as e:
        print("Error al leer el archivo STL:", e)