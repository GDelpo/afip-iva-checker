from typing import List, Tuple

from core.field_calculator import detect_total_differences
from core.string_utils import format_numeric_string
from logger import logger


def format_difference(data: Tuple) -> Tuple:
    """
    Formatea una tupla de diferencia para su uso posterior.

    Args:
        data: Tupla con (índice, monto calculado, monto original)

    Returns:
        Tupla formateada
    """
    # Validar que data sea una tupla y tenga 3 elementos
    if not isinstance(data, tuple) or len(data) != 3:
        error_msg = "Input must be a tuple with exactly 3 elements."
        logger.error(error_msg)
        raise ValueError(error_msg)

    index, total_summed_amount, original_amount = data
    logger.debug(
        f"Formateando diferencia: línea={index}, calculado={total_summed_amount}, original={original_amount}"
    )

    # Formatear los valores usando format_numeric_string
    formatted_summed = format_numeric_string(total_summed_amount, 15)
    formatted_original = format_numeric_string(original_amount, 15)
    logger.debug(
        f"Valores formateados: calculado='{formatted_summed}', original='{formatted_original}'"
    )

    # Retornar la tupla con los valores procesados
    return index, formatted_summed, formatted_original


def format_differences(list_of_tuples: List[Tuple]) -> List[Tuple]:
    """
    Formatea una lista de tuplas de diferencias.

    Args:
        list_of_tuples: Lista de tuplas con diferencias

    Returns:
        Lista de tuplas formateadas
    """
    logger.info(f"Formateando {len(list_of_tuples)} tuplas de diferencias")
    # Usar list comprehension para procesar cada tupla
    return [format_difference(item) for item in list_of_tuples]


def format_total_differences(merged_books: dict, book_key: str) -> list:
    """
    Finds and formats the total differences between calculated and original values.

    Args:
        merged_books (dict): Merged data from both books.
        book_key (str): Key for the book to compare against totals.

    Returns:
        list: List of formatted difference tuples.
    """
    differences = detect_total_differences(merged_books, book_key)
    return format_differences(differences)
