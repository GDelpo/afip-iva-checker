from typing import List, Tuple

from core.book_merger import merge_and_summarize
from core.book_parser import parse_book_file
from core.diff_formatter import format_total_differences
from core.error_document_mapper import detect_and_prepare_error_documents
from core.exceptions import ProcessingError
from core.file_writer import write_replacements
from core.report_generator import generate_final_report
from logger import logger


def _gather_differences(
    merged_books: dict, book_key: str
) -> List[Tuple[int, str, str]]:
    """
    Combina diferencias de totales y documentos erróneos en una sola lista.
    """
    # Diferencias de totales numéricos
    total_diffs = format_total_differences(merged_books, book_key)
    # Diferencias de documentos (errores AFIP)
    doc_diffs = detect_and_prepare_error_documents(merged_books, book_key)
    return total_diffs + doc_diffs


def _apply_differences(
    differences: List[Tuple[int, str, str]], source_file: str, output_folder: str
) -> None:
    """
    Escribe las líneas modificadas según las diferencias encontradas.
    """
    logger.info(f"Reemplazando {len(differences)} valores en {source_file}")
    write_replacements(differences, source_file, output_folder)


def run_book_comparison(
    book_1_file_path: str,
    book_1_key: str,
    book_2_file_path: str,
    book_2_key: str,
    output_folder_path: str,
) -> Tuple[bool, str]:
    """
    Realiza el proceso completo de comparación entre dos libros IVA.
    """
    logger.info(
        f"Iniciando proceso de unificación y fix sobre: {book_1_key} y {book_2_key}"
    )

    try:
        # Parseo de archivos
        book_1_lines = parse_book_file(book_1_file_path, book_1_key)
        book_2_lines = parse_book_file(book_2_file_path, book_2_key)

        # Validación de longitud
        if len(book_1_lines) != len(book_2_lines):
            diff = abs(len(book_1_lines) - len(book_2_lines))
            msg = (
                f"Longitudes difieren en {diff} líneas: "
                f"{book_1_key} tiene {len(book_1_lines)}, "
                f"{book_2_key} tiene {len(book_2_lines)}."
            )
            logger.error(msg)
            raise ProcessingError(msg)

        # Fusión y cálculo
        merged = merge_and_summarize(book_1_lines, book_2_lines, book_1_key, book_2_key)

        # Recolectar y aplicar diferencias
        differences = _gather_differences(merged, book_1_key)
        if differences:
            _apply_differences(differences, book_1_file_path, output_folder_path)
        else:
            logger.info("No se encontraron diferencias entre los libros.")

        # Generar reporte final
        message = generate_final_report(merged, differences, output_folder_path, False)
        logger.info(f"Proceso completado exitosamente\n{'-' * 50}")
        return True, message

    except ProcessingError as e:
        logger.error(f"Error de procesamiento: {e.message}")
        raise
    except Exception as e:
        msg = f"Error inesperado: {e}"
        logger.exception(msg)
        raise ProcessingError(msg)
