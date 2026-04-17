from typing import Dict, List, Optional, Tuple, Union

from logger import logger


def extract_substring_value(
    data_string: str, positions: Union[Tuple[int, int], Tuple[int]]
) -> str:
    """
    Extrae un valor de una cadena según las posiciones especificadas.

    Args:
        data_string: Cadena de datos
        positions: Tupla con posiciones de inicio y fin, o solo inicio

    Returns:
        Valor extraído
    """
    try:
        if len(positions) == 2:
            start_position, end_position = positions
            extracted = data_string[start_position : end_position + 1]
            logger.debug(f"Valor extraído de posiciones {positions}: '{extracted}'")
            return extracted
        else:
            start_position = positions[0]
            extracted = data_string[start_position]
            logger.debug(f"Valor extraído de posición {start_position}: '{extracted}'")
            return extracted
    except (IndexError, TypeError) as e:
        logger.error(f"Error al extraer valor de posiciones {positions}: {e}")
        return ""


def format_field_value(value: str, decimal_index: int) -> str:
    """
    Formatea un valor añadiendo punto decimal en la posición correcta.

    Args:
        value: Valor a formatear
        decimal_index: Índice para la parte decimal

    Returns:
        Valor formateado
    """
    try:
        value = value.strip()
        integer_part = value[:-decimal_index]
        decimal_part = value[-decimal_index:]
        formatted = f"{int(integer_part)}.{decimal_part}"
        logger.debug(f"Valor formateado: {value} -> {formatted}")
        return formatted
    except (IndexError, ValueError) as e:
        logger.error(
            f"Error al formatear valor {value} con índice decimal {decimal_index}: {e}"
        )
        return value


def extract_and_format_fields(data_string: str, field_structure: Dict) -> Dict:
    """
    Extrae valores de una cadena de acuerdo a una estructura de campo definida, aplicando
    formateo para los casos de decimales sin punto (13 enteros y 2 decimales, 4 enteros y 6 decimales).

    Args:
        data_string: Cadena de datos que contiene los valores a extraer.
        field_structure: Diccionario que define las posiciones y observaciones de cada campo.

    Returns:
        dict: Un diccionario que contiene el número de campo, el nombre y el valor formateado.
    """
    logger.debug(f"Extrayendo valores de línea de longitud {len(data_string)}")
    extracted_values = {}

    for field_number, field_info in field_structure.items():
        field_positions = field_info["Posiciones"]
        field_name = field_info["Campo"]
        field_observations = field_info.get(
            "Observaciones"
        )  # Usamos .get() para evitar errores si no hay observaciones

        field_value = extract_substring_value(data_string, field_positions)
        logger.debug(
            f"Campo {field_number} ({field_name}): valor extraído '{field_value}'"
        )

        # Verificamos si hay observaciones que requieren un formato específico
        if field_observations:
            decimal_index = None

            if field_observations == "13 enteros 2 decimales sin punto decimal":
                decimal_index = 2  # Para valores con 13 enteros y 2 decimales
            elif field_observations == "4 enteros 6 decimales sin punto decimal":
                decimal_index = 6  # Para valores con 4 enteros y 6 decimales
            elif field_observations == "Completar con ceros a la izquierda":
                field_value = field_value.lstrip("0")
                logger.debug(
                    f"Campo {field_number}: eliminando ceros a la izquierda -> '{field_value}'"
                )

            if decimal_index is not None:
                # Formateamos el valor como un número decimal
                field_value = format_field_value(field_value, decimal_index)

        # Guardamos el resultado en el diccionario de valores extraídos
        extracted_values[field_number] = {
            "field_name": field_name,
            "value": field_value.strip(),
        }  # Elimina espacios adicionales

    return extracted_values


def extract_document_ids(
    merged_dict: Dict, book_key: str, field_number: int = 7
) -> List[Optional[int]]:
    """
    Encuentra documentos en un diccionario fusionado según un campo específico
    y los devuelve como valores enteros, o None cuando no se pueda convertir.

    Args:
        merged_dict: Diccionario fusionado con datos de ambos libros
        book_key: Clave del libro en el que buscar documentos
        field_number: Número del campo que contiene los documentos

    Returns:
        Lista que contiene enteros o None para los documentos encontrados
    """
    logger.info(f"Buscando documentos en el campo {field_number} del libro {book_key}")
    list_of_docs = []
    count_valid = 0
    count_invalid = 0

    for key, value in merged_dict.items():
        # Obtener el valor del campo especificado en el libro proporcionado
        if book_key in value:
            field_data = value[book_key].get(field_number, {})
            field_value = field_data.get("value")

            if field_value is not None:
                try:
                    # Intentar convertir a entero, eliminando posibles espacios
                    doc_id = int(str(field_value).strip())
                    list_of_docs.append(doc_id)
                    count_valid += 1
                    logger.debug(f"Documento encontrado en línea {key}: {doc_id}")
                except (ValueError, TypeError):
                    # Si no se puede convertir, agregar None y registrar el error
                    list_of_docs.append(0)
                    count_invalid += 1
                    logger.warning(
                        f"No se pudo convertir a entero el valor '{field_value}' en línea {key}"
                    )
            else:
                # Si no hay valor, agregar None para mantener correspondencia con índices
                list_of_docs.append(0)
                count_invalid += 1
                logger.debug(f"No se encontró valor en la línea {key}")

    logger.info(
        f"Total de documentos encontrados: {len(list_of_docs)} (válidos: {count_valid}, inválidos: {count_invalid})"
    )
    return list_of_docs
