#!/usr/bin/env python3
"""
Módulo: scale_db.py

Este módulo maneja la base de datos destinada a guardar escalas de medida
de diversos objetos para permitir conversiones de escalas (por ejemplo, de 1:1 a 1:36).
Utiliza SQLite para almacenar registros que incluyen:
  - object_name: Nombre del objeto o modelo.
  - original_scale: Escala original (por ejemplo, "1:1").
  - desired_scale: Escala deseada (por ejemplo, "1:36").
  - conversion_factor: Factor de conversión numérico (por ejemplo, 1/36).
  - notes: Notas adicionales (opcional).
"""

import sqlite3
import logging
from sqlite3 import Connection, Cursor, Error
from pathlib import Path
from typing import Any, Dict, List, Optional

# Importar la configuración de logging desde logger_config.py
from logger_config import setup_logger

# Importar la configuración para obtener la ruta de la base de datos
from settings import DB_PATH

# Obtener un logger para este módulo.
logger = setup_logger(name=__name__, level=logging.DEBUG, log_file="logs/scale_db.log")

class ScaleDB:
    """
    Clase para interactuar con la base de datos de escalas.

    Permite crear la tabla 'scales' (si no existe) y realizar operaciones
    de inserción, consulta, actualización y eliminación de registros.
    """

    def __init__(self, db_path: Path = DB_PATH) -> None:
        self.db_path = db_path
        try:
            self.conn: Connection = sqlite3.connect(str(self.db_path))
            logger.info("Conexión a la base de datos establecida en %s", self.db_path)
            self._create_table()
        except Error as e:
            logger.exception("Error al conectar con la base de datos: %s", e)
            raise

    def _create_table(self) -> None:
        """
        Crea la tabla 'scales' si no existe.
        """
        create_table_sql = """
        CREATE TABLE IF NOT EXISTS scales (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            object_name TEXT NOT NULL,
            original_scale TEXT NOT NULL,
            desired_scale TEXT NOT NULL,
            conversion_factor REAL NOT NULL,
            notes TEXT
        );
        """
        try:
            with self.conn:
                cur: Cursor = self.conn.cursor()
                cur.execute(create_table_sql)
                logger.info("Tabla 'scales' verificada/creada correctamente.")
        except Error as e:
            logger.exception("Error al crear la tabla 'scales': %s", e)
            raise

    def add_scale(
        self,
        object_name: str,
        original_scale: str,
        desired_scale: str,
        conversion_factor: float,
        notes: Optional[str] = None,
    ) -> int:
        """
        Inserta un nuevo registro en la tabla 'scales'.

        Args:
            object_name (str): Nombre del objeto (por ejemplo, "Modelo de Auto").
            original_scale (str): Escala original, por ejemplo "1:1".
            desired_scale (str): Escala a la que se desea convertir, por ejemplo "1:36".
            conversion_factor (float): Factor de conversión (ejemplo, 1/36 para 1:1 a 1:36).
            notes (Optional[str]): Notas adicionales.

        Returns:
            int: El ID del registro insertado.
        """
        insert_sql = """
        INSERT INTO scales (object_name, original_scale, desired_scale, conversion_factor, notes)
        VALUES (?, ?, ?, ?, ?);
        """
        try:
            with self.conn:
                cur: Cursor = self.conn.cursor()
                cur.execute(
                    insert_sql,
                    (object_name, original_scale, desired_scale, conversion_factor, notes),
                )
                new_id = cur.lastrowid
                logger.info("Registro insertado con ID: %d", new_id)
                return new_id
        except Error as e:
            logger.exception("Error al insertar la escala: %s", e)
            raise Exception(f"Error al insertar la escala: {e}")

    def get_scale_by_id(self, scale_id: int) -> Optional[Dict[str, Any]]:
        """
        Recupera un registro de escala por su ID.

        Args:
            scale_id (int): ID del registro.

        Returns:
            Optional[Dict[str, Any]]: Un diccionario con los datos del registro
                                      o None si no se encuentra.
        """
        query_sql = "SELECT * FROM scales WHERE id = ?;"
        try:
            cur: Cursor = self.conn.cursor()
            cur.execute(query_sql, (scale_id,))
            row = cur.fetchone()
            if row:
                logger.info("Registro con ID %d recuperado.", scale_id)
                return {
                    "id": row[0],
                    "object_name": row[1],
                    "original_scale": row[2],
                    "desired_scale": row[3],
                    "conversion_factor": row[4],
                    "notes": row[5],
                }
            logger.warning("Registro con ID %d no encontrado.", scale_id)
            return None
        except Error as e:
            logger.exception("Error al recuperar el registro con ID %d: %s", scale_id, e)
            raise

    def get_all_scales(self) -> List[Dict[str, Any]]:
        """
        Recupera todos los registros de la tabla 'scales'.

        Returns:
            List[Dict[str, Any]]: Una lista de diccionarios con cada registro.
        """
        query_sql = "SELECT * FROM scales;"
        try:
            cur: Cursor = self.conn.cursor()
            cur.execute(query_sql)
            rows = cur.fetchall()
            logger.info("Recuperados %d registros de escalas.", len(rows))
            return [
                {
                    "id": row[0],
                    "object_name": row[1],
                    "original_scale": row[2],
                    "desired_scale": row[3],
                    "conversion_factor": row[4],
                    "notes": row[5],
                }
                for row in rows
            ]
        except Error as e:
            logger.exception("Error al recuperar todos los registros: %s", e)
            raise

    def update_scale(
        self,
        scale_id: int,
        object_name: Optional[str] = None,
        original_scale: Optional[str] = None,
        desired_scale: Optional[str] = None,
        conversion_factor: Optional[float] = None,
        notes: Optional[str] = None,
    ) -> None:
        """
        Actualiza un registro de escala especificado por su ID.

        Args:
            scale_id (int): ID del registro a actualizar.
            object_name (Optional[str]): Nuevo nombre del objeto.
            original_scale (Optional[str]): Nueva escala original.
            desired_scale (Optional[str]): Nueva escala deseada.
            conversion_factor (Optional[float]): Nuevo factor de conversión.
            notes (Optional[str]): Nuevas notas.
        """
        updates = []
        values = []
        if object_name is not None:
            updates.append("object_name = ?")
            values.append(object_name)
        if original_scale is not None:
            updates.append("original_scale = ?")
            values.append(original_scale)
        if desired_scale is not None:
            updates.append("desired_scale = ?")
            values.append(desired_scale)
        if conversion_factor is not None:
            updates.append("conversion_factor = ?")
            values.append(conversion_factor)
        if notes is not None:
            updates.append("notes = ?")
            values.append(notes)

        if not updates:
            logger.info("No se realizaron cambios para el registro con ID %d.", scale_id)
            return  # No hay cambios a actualizar

        update_sql = f"UPDATE scales SET {', '.join(updates)} WHERE id = ?;"
        values.append(scale_id)
        try:
            with self.conn:
                cur: Cursor = self.conn.cursor()
                cur.execute(update_sql, tuple(values))
                logger.info("Registro con ID %d actualizado.", scale_id)
        except Error as e:
            logger.exception("Error al actualizar el registro con ID %d: %s", scale_id, e)
            raise

    def delete_scale(self, scale_id: int) -> None:
        """
        Elimina un registro de la tabla 'scales' por su ID.

        Args:
            scale_id (int): ID del registro a eliminar.
        """
        delete_sql = "DELETE FROM scales WHERE id = ?;"
        try:
            with self.conn:
                cur: Cursor = self.conn.cursor()
                cur.execute(delete_sql, (scale_id,))
                logger.info("Registro con ID %d eliminado.", scale_id)
        except Error as e:
            logger.exception("Error al eliminar el registro con ID %d: %s", scale_id, e)
            raise

    def close(self) -> None:
        """
        Cierra la conexión con la base de datos.
        """
        try:
            self.conn.close()
            logger.info("Conexión a la base de datos cerrada.")
        except Error as e:
            logger.exception("Error al cerrar la conexión a la base de datos: %s", e)
            raise


# Ejemplo de uso:
if __name__ == "__main__":
    db = ScaleDB()
    try:
        # Ejemplo: insertar un registro de escala, de 1:1 a 1:36.
        new_id = db.add_scale(
            object_name="Modelo de Ejemplo",
            original_scale="1:1",
            desired_scale="1:36",
            conversion_factor=1 / 36,
            notes="Escala estándar para miniaturas.",
        )
        print("Registro insertado con ID:", new_id)

        # Consultar el registro insertado.
        record = db.get_scale_by_id(new_id)
        print("Registro recuperado:")
        print(record)

        # Listar todos los registros guardados.
        all_records = db.get_all_scales()
        print("Todos los registros de escalas:")
        for rec in all_records:
            print(rec)
    finally:
        db.close()