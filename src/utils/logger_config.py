#!/usr/bin/env python3
"""
Módulo: logger_config.py

Este módulo configura y provee loggers para el proyecto. 
Permite obtener un logger con:
  - Salida a consola.
  - Salida a un archivo (opcional) en la carpeta 'logs'.
  
El módulo es genérico y puede ser utilizado en cualquier parte del proyecto
para registrar mensajes con niveles INFO, DEBUG, WARNING, ERROR o CRITICAL.
"""

import logging
import os
from pathlib import Path
from typing import Optional

def setup_logger(
    name: str = __name__,
    level: int = logging.INFO,
    log_file: Optional[str] = None
) -> logging.Logger:
    """
    Configura y retorna un logger con el nombre, nivel y salida especificados.
    
    Si se proporciona 'log_file', se creará un FileHandler para escribir
    los logs en ese archivo (asegurándose de que el directorio exista).

    Args:
        name (str): Nombre del logger.
        level (int): Nivel del logger (por ejemplo, logging.INFO).
        log_file (Optional[str]): Ruta del archivo de log. Si es None, 
                                  solo se configurará la salida a consola.
    
    Returns:
        logging.Logger: Logger configurado.
    """
    logger = logging.getLogger(name)
    logger.setLevel(level)
    
    # Evitar agregar múltiples handlers si el logger ya está configurado.
    if logger.handlers:
        return logger

    formatter = logging.Formatter('[%(asctime)s][%(name)s][%(levelname)s] %(message)s')

    # Configurar Handler para consola.
    console_handler = logging.StreamHandler()
    console_handler.setLevel(level)
    console_handler.setFormatter(formatter)
    logger.addHandler(console_handler)

    # Configurar FileHandler si se proporciona log_file.
    if log_file:
        # Asegurarse de que el directorio para el archivo exista.
        log_path = Path(log_file)
        if not log_path.parent.exists():
            log_path.parent.mkdir(parents=True, exist_ok=True)
        file_handler = logging.FileHandler(str(log_path))
        file_handler.setLevel(level)
        file_handler.setFormatter(formatter)
        logger.addHandler(file_handler)

    logger.propagate = False  # Evita que los mensajes se dupliquen en loggers raíz.
    return logger

# Ejemplo de uso:
if __name__ == "__main__":
    # Obtén un logger que escriba en consola y en un archivo de logs.
    log = setup_logger(name="EjemploLogger", level=logging.DEBUG, log_file="logs/proyecto.log")
    log.debug("Mensaje DEBUG de prueba.")
    log.info("Mensaje INFO de prueba.")
    log.warning("Mensaje de WARNING de prueba.")
    log.error("Mensaje ERROR de prueba.")
    log.critical("Mensaje CRITICAL de prueba.")