from .models import BOOKS


def retrieve_keys_to_sum(name_of_book):
    list_of_keys = []

    match name_of_book:
        case "libro_iva_digital_ventas_cbte":
            list_of_keys = [10, 11, 12, 13, 14, 15, 16, 21]
        case "libro_iva_digital_ventas_alicuota":
            list_of_keys = [4, 6]
        case "libro_iva_digital_compras_cbte":
            list_of_keys = [10, 11, 12, 13, 14, 15, 16, 21, 22, 25]
        case "libro_iva_digital_compras_alicuota":
            list_of_keys = [6, 8]

    return list_of_keys


def retrieve_field_structure(name_of_book):
    return BOOKS[name_of_book]


def retrieve_expected_length(name_of_book):
    len_of_book = 0
    match name_of_book:
        case "libro_iva_digital_ventas_cbte":
            len_of_book = 266
        case "libro_iva_digital_ventas_alicuota":
            len_of_book = 62
        case "libro_iva_digital_compras_cbte":
            len_of_book = 325
        case "libro_iva_digital_compras_alicuota":
            len_of_book = 84
    return len_of_book
