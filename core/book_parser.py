from typing import Dict, List

from core.exceptions import ProcessingError
from core.field_calculator import calculate_field_totals
from core.value_extractor import extract_and_format_fields
from logger import logger
from models.book_utils import (
    retrieve_expected_length,
    retrieve_field_structure,
    retrieve_keys_to_sum,
)


def parse_book_file(file_name: str, name_of_book: str) -> List[Dict]:
    """
    Procesa un archivo de libro IVA, extrayendo y calculando valores.

    Args:
        file_name: Ruta al archivo a procesar
        name_of_book: Clave del tipo de libro

    Returns:
        Lista de diccionarios con los datos procesados
    """
    logger.info(f"Procesando archivo {file_name} como {name_of_book}")
    list_of_data = []
    try:
        expected_length = retrieve_expected_length(name_of_book)
        logger.debug(
            f"Longitud esperada para {name_of_book}: {expected_length} caracteres"
        )

        with open(file_name, "r") as file:
            for index, line in enumerate(file, start=1):
                logger.debug(f"Procesando línea {index} (longitud: {len(line) - 1})")

                # Verificar longitud de línea
                if len(line) - 1 != expected_length:
                    error_msg = (
                        f"La longitud de la línea {index} no coincide con la longitud esperada para el libro {name_of_book}. "
                        f"Longitud actual: {len(line)}, longitud esperada: {expected_length}"
                    )
                    logger.error(error_msg)
                    raise ProcessingError(error_msg)

                # Procesar línea
                line = line.strip()
                book_structure = retrieve_field_structure(name_of_book)
                extracted_values = extract_and_format_fields(line, book_structure)

                # Calcular totales
                keys_to_sum = retrieve_keys_to_sum(name_of_book)
                calculated_values = calculate_field_totals(
                    extracted_values, keys_to_sum
                )

                # Guardar resultados
                dict_of_line = {str(index): calculated_values}
                list_of_data.append(dict_of_line)
                logger.debug(f"Línea {index} procesada correctamente")

        logger.info(f"Archivo procesado. Total de líneas: {len(list_of_data)}")
        return list_of_data

    except FileNotFoundError:
        error_msg = f"No se encontró el archivo {file_name}."
        logger.error(error_msg)
        raise ProcessingError(error_msg)
    except ProcessingError as e:
        logger.error(f"Error de procesamiento: {e.message}")
        raise e
    except Exception as e:
        error_msg = f"Ocurrió un error inesperado: {str(e)}"
        logger.exception(error_msg)
        raise ProcessingError(error_msg) from e
