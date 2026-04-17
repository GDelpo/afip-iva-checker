import math

from logger import logger


def pad_left(str_value: str, len_of_str: int) -> str:
    """
    Formatea un valor string a una longitud específica, rellenando con ceros a la izquierda.

    Args:
        str_value: Valor string a formatear
        len_of_str: Longitud del string resultante

    Returns:
        Cadena formateada
    """
    if len(str_value) < len_of_str:
        diff = len_of_str - len(str_value)
        str_value = f"{'0' * diff}{str_value}"

    return str_value


def format_numeric_string(value: float, len_of_str: int) -> str:
    """
    Formatea un valor numérico según el formato requerido por AFIP.

    Args:
        value: Valor numérico a formatear
        len_of_str: Longitud del string resultante

    Returns:
        Cadena formateada
    """
    try:
        # Descomponer el valor en parte decimal y parte entera
        decimals, integer = math.modf(value)

        # Redondear la parte decimal a dos decimales
        decimals = abs(round(decimals, 2))

        # Convertir a string y eliminar el punto decimal
        str_value = f"{int(integer)}{str(decimals)[2:].ljust(2, '0')}"

        # Ajustar a longitud
        if len(str_value) < len_of_str:
            str_value = pad_left(str_value, len_of_str)

        return str_value

    except (ValueError, TypeError) as e:
        logger.error(f"Error al formatear valor {value}: {e}")
        return None
