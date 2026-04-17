import os
from typing import List, Tuple

from logger import logger


def write_replacements(
    list_of_values: List[Tuple], file_name: str, output_path: str
) -> None:
    """
    Reemplaza valores en un archivo según una lista de tuplas con diferencias.

    Args:
        list_of_values: Lista de tuplas con diferencias (línea, valor nuevo, valor original)
        file_name: Ruta al archivo a modificar
        output_path: Ruta donde guardar el archivo modificado
    """
    logger.info(f"Reemplazando las lineas en el archivo: '{file_name}'")
    logger.debug(
        f"Parámetros recibidos: {len(list_of_values)} reemplazos, output_path='{output_path}'"
    )

    try:
        # Comprobar que el archivo existe
        if not os.path.isfile(file_name):
            logger.error(f"El archivo no existe: {file_name}")
            return

        # Leer todas las líneas del archivo
        logger.debug("Abriendo archivo para lectura")
        with open(file_name, "r", encoding="ISO-8859-1") as file:
            lines = file.readlines()
        logger.debug(f"Archivo leído correctamente: {len(lines)} líneas cargadas")

        # Reemplazar las líneas según los valores de la lista
        replacements_count = 0
        for idx, (line_num, new_value, old_value) in enumerate(list_of_values, start=1):
            logger.debug(
                f"[Item {idx}] Procesando tupla: línea={line_num}, old='{old_value}', new='{new_value}'"
            )
            line_index = int(line_num) - 1

            if 0 <= line_index < len(lines):
                if old_value in lines[line_index]:
                    before = lines[line_index].rstrip("\n")
                    lines[line_index] = lines[line_index].replace(old_value, new_value)
                    after = lines[line_index].rstrip("\n")
                    replacements_count += 1
                    logger.debug(
                        f"  → Reemplazo OK en línea {line_num}: '{before}'  →  '{after}'"
                    )
                else:
                    logger.warning(
                        f"  ⚠️ No encontrado en línea {line_num}: '{old_value}'"
                    )
            else:
                logger.warning(
                    f"  ⚠️ Índice fuera de rango: {line_index} (válido: 0–{len(lines) - 1})"
                )

        # Asegurarse de que la carpeta de salida exista
        if not os.path.isdir(output_path):
            try:
                os.makedirs(output_path, exist_ok=True)
                logger.debug(f"Carpeta de salida creada: {output_path}")
            except Exception as e:
                logger.error(f"Error al crear carpeta de salida '{output_path}': {e}")
                raise

        # Generar nombre del archivo modificado
        base = os.path.basename(file_name)
        name, ext = os.path.splitext(base)
        modified_file_name = os.path.join(
            output_path, f"{name}_modificated{ext or '.txt'}"
        )
        logger.debug(f"Nombre del archivo de salida: {modified_file_name}")

        # Escribir las líneas modificadas
        with open(modified_file_name, "w", encoding="ISO-8859-1") as file:
            file.writelines(lines)
        logger.info(f"Archivo modificado guardado en '{modified_file_name}'")
        logger.info(f"Total de reemplazos realizados: {replacements_count}")

        if replacements_count == 0:
            logger.info(
                "No se realizó ningún reemplazo. Verifica las tuplas de entrada."
            )

    except Exception as e:
        logger.exception(f"[ERROR] write_replacements falló: {e}")
        raise
