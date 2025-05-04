Reescalador STL Moderno
========================

Descripción
------------
Este programa permite trabajar con archivos STL, proporcionando una herramienta para reescalar modelos 3D, visualizar sus propiedades y guardar copias modificadas. Su interfaz gráfica interactiva facilita la manipulación de archivos, mientras que la visualización avanzada permite inspeccionar los detalles del modelo.

Características
---------------
1. Selección de archivo STL: Carga cualquier archivo STL desde tu sistema.
2. Reescalado: Ajusta el tamaño del modelo aplicando un factor de escala personalizado.
3. Visualización interactiva: Visualiza el modelo en 3D con controles como zoom y ajustes de cámara.
4. Transparencia opcional: Permite ver el modelo con o sin transparencia.
5. Propiedades del modelo: Muestra dimensiones, volumen, área total y número de triángulos.
6. Guardado: Exporta el modelo modificado sin sobrescribir el original.
7. Ejecutable disponible: Para facilitar su uso, se proporciona un archivo ejecutable (.exe) listo para ejecutar en sistemas Windows.

Requisitos
----------
- Python 3.8 o superior
- Librerías necesarias:
  - wxPython
  - numpy
  - pyvista
  - numpy-stl

Instalación
-----------
1. Asegúrate de que Python esté instalado en tu sistema.
2. Instala las dependencias ejecutando el siguiente comando en tu terminal:
3. Guarda el código fuente en un archivo llamado `reescalador_stl.py`.

Ejecutar el programa
--------------------
1. Abre tu terminal.
2. Navega a la ubicación donde guardaste el archivo.
3. Ejecuta el siguiente comando:


O bien, simplemente ejecuta el archivo `.exe` proporcionado para una experiencia más sencilla.

Nota importante sobre el ejecutable
-----------------------------------
- Algunos antivirus pueden marcar el archivo ejecutable (.exe) como sospechoso, debido a la manera en que se empaquetan los recursos. Esto no significa que el archivo sea dañino.
- Asegúrate de descargar el ejecutable desde una fuente confiable (por ejemplo, directamente de ti como desarrollador).
- Si el antivirus detecta una alerta, permite manualmente su ejecución añadiendo el archivo a la lista de excepciones de tu antivirus.

Uso
---
1. Haz clic en "Seleccionar" para cargar un archivo STL.
2. Introduce el factor de escala (Ejemplo: 1.5) y haz clic en "Aplicar Escala".
3. Usa "Visualizar Modelo" para inspeccionar el modelo en 3D.
4. Marca o desmarca "Mostrar Transparencias" para ajustar el estilo de la visualización.
5. Guarda el modelo modificado con el botón "Guardar Modelo".

Controles en la visualización
-----------------------------
- Restablecer cámara: Presiona la tecla `R`.
- Acercar zoom: Presiona la tecla `+`.
- Alejar zoom: Presiona la tecla `-`.

Notas
-----
- El archivo ejecutable está diseñado específicamente para sistemas Windows y elimina la necesidad de instalar Python.
- Este programa es personalizable y puedes adaptarlo según tus necesidades.
