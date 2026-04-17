from collections import OrderedDict
from typing import Dict, List

from logger import logger


def append_total_sums(
    merged_dict: OrderedDict, book_1_key: str, book_2_key: str
) -> OrderedDict:
    """
    Añade los totales sumados de ambos libros a un diccionario fusionado.

    Args:
        merged_dict: Diccionario fusionado con datos de ambos libros
        book_1_key: Clave del primer libro
        book_2_key: Clave del segundo libro

    Returns:
        Diccionario ordenado con los totales sumados añadidos
    """
    logger.info("Calculando totales sumados para el diccionario fusionado")

    for key, value in merged_dict.items():
        total_sum = 0

        # Sumar los valores de summed_amounts en el primer libro
        if book_1_key in value:
            book1_summed_amounts = value[book_1_key].get("summed_amounts", {})
            book1_total = book1_summed_amounts.get("total", 0)
            total_sum += book1_total
            logger.debug(f"Línea {key}: total de {book_1_key} = {book1_total}")

        # Sumar los valores de summed_amounts en el segundo libro
        if book_2_key in value:
            book2_summed_amounts = value[book_2_key].get("summed_amounts", {})
            book2_total = book2_summed_amounts.get("total", 0)
            total_sum += book2_total
            logger.debug(f"Línea {key}: total de {book_2_key} = {book2_total}")

        # Agregar el total sumado en el diccionario principal
        rounded_total = round(total_sum, 2)
        value["total_summed_amount"] = rounded_total
        logger.debug(f"Línea {key}: total sumado = {rounded_total}")

    logger.info("Totales sumados calculados correctamente")
    return merged_dict


def merge_books_by_line(
    dict_list_1: List[Dict], dict_list_2: List[Dict], book_1_key: str, book_2_key: str
) -> OrderedDict:
    """
    Fusiona dos listas de diccionarios en un único diccionario ordenado por número de línea.

    Args:
        dict_list_1: Primera lista de diccionarios
        dict_list_2: Segunda lista de diccionarios
        book_1_key: Clave para identificar la primera lista
        book_2_key: Clave para identificar la segunda lista

    Returns:
        Diccionario ordenado con los datos fusionados
    """
    logger.info(f"Fusionando libros {book_1_key} y {book_2_key}")
    merged_dict = OrderedDict()

    # Recorrer la primera lista de diccionarios
    for item_1 in dict_list_1:
        for key, value in item_1.items():
            if key not in merged_dict:
                merged_dict[key] = OrderedDict()
            merged_dict[key][book_1_key] = value
            logger.debug(f"Agregando línea {key} de {book_1_key}")

    # Recorrer la segunda lista de diccionarios
    for item_2 in dict_list_2:
        for key, value in item_2.items():
            if key in merged_dict:
                merged_dict[key][book_2_key] = value
                logger.debug(f"Agregando línea {key} de {book_2_key} (existente)")
            else:
                merged_dict[key] = OrderedDict()
                merged_dict[key][book_2_key] = value
                logger.debug(f"Agregando línea {key} de {book_2_key} (nueva)")

    logger.info(f"Fusión completada. Total de líneas: {len(merged_dict)}")
    return merged_dict


def merge_and_summarize(
    dict_list_1: List[Dict], dict_list_2: List[Dict], book_1_key: str, book_2_key: str
) -> OrderedDict:
    """
    Fusiona dos listas de diccionarios y añade los totales sumados.

    Args:
        dict_list_1: Primera lista de diccionarios
        dict_list_2: Segunda lista de diccionarios
        book_1_key: Clave para identificar la primera lista
        book_2_key: Clave para identificar la segunda lista

    Returns:
        Diccionario ordenado con los datos fusionados y totales calculados
    """
    merged_books = merge_books_by_line(dict_list_1, dict_list_2, book_1_key, book_2_key)
    merged_books = append_total_sums(merged_books, book_1_key, book_2_key)
    return merged_books
