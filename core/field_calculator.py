from typing import Dict, List, Tuple

from logger import logger


def calculate_field_totals(data_dict: Dict[int, Dict], keys_to_sum: List[int]) -> Dict:
    """
    Calcula los totales sumando los valores de campos específicos.

    Args:
        data_dict: Diccionario con los datos de una línea
        keys_to_sum: Lista de claves cuyos valores deben sumarse

    Returns:
        Diccionario actualizado con el total sumado
    """
    logger.debug(f"Calculando totales para claves: {keys_to_sum}")
    total_sum = 0
    for key in keys_to_sum:
        if key in data_dict and "value" in data_dict[key]:
            value = float(data_dict[key]["value"])
            total_sum += value
            logger.debug(f"Campo {key}: {value}")
        else:
            logger.warning(f"Clave {key} no encontrada para sumar")

    rounded_total = round(total_sum, 2)
    logger.debug(f"Total calculado: {rounded_total}")

    data_dict["summed_amounts"] = {
        "referenced_fields": ", ".join(map(str, keys_to_sum)).strip(),
        "total": rounded_total,
    }

    return data_dict


def compute_difference(value1: float, value2: float) -> float:
    """
    Calcula la diferencia absoluta entre dos valores.

    Args:
        value1: Primer valor
        value2: Segundo valor

    Returns:
        Diferencia absoluta
    """
    return abs(value1 - value2)


def is_difference_significant(
    value1: float, value2: float, threshold: float = 1
) -> bool:
    """
    Verifica si la diferencia entre dos valores excede un umbral.

    Args:
        value1: Primer valor
        value2: Segundo valor
        threshold: Umbral de diferencia aceptable

    Returns:
        True si la diferencia excede el umbral, False en caso contrario
    """
    return compute_difference(value1, value2) > threshold


def detect_total_differences(
    merged_dict: Dict[str, Dict], book_key: str, field_number: int = 9
) -> List[Tuple]:
    """
    Encuentra diferencias entre los totales calculados y los valores en un campo específico.

    Args:
        merged_dict: Diccionario fusionado con datos de ambos libros
        book_key: Clave del libro en el que buscar diferencias
        field_number: Número del campo a comparar con el total calculado

    Returns:
        Lista de tuplas con diferencias encontradas (línea, valor calculado, valor actual)
    """
    logger.info(f"Buscando diferencias en el campo {field_number} del libro {book_key}")
    differences = []

    for key, value in merged_dict.items():
        # Obtener el total_summed_amount
        total_summed_amount = value.get("total_summed_amount", 0)

        # Obtener el valor del campo especificado en el libro proporcionado
        field_value = None
        if book_key in value:
            field_data = value[book_key].get(field_number, {})
            field_value = float(field_data.get("value", 0))

        # Comparar los valores
        if field_value is not None and total_summed_amount != field_value:
            diff = compute_difference(total_summed_amount, field_value)
            if is_difference_significant(total_summed_amount, field_value):
                logger.debug(
                    f"Diferencia encontrada en línea {key}: calculado={total_summed_amount}, actual={field_value}, diff={diff}"
                )
                # Si no coinciden, añadir una tupla con: número de fila (key), total_summed_amount, y field_value
                differences.append((int(key), total_summed_amount, field_value))

    logger.debug(f"Diferencias encontradas: {differences}")
    logger.info(f"Total de diferencias encontradas: {len(differences)}")
    return differences
