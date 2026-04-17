from afip_client.error_detector import detect_invalid_documents
from core.string_utils import pad_left
from core.value_extractor import extract_document_ids


def get_replacement_document_id(document: str) -> str:
    """
    Reemplaza el valor de un documento con un nuevo valor.

    Args:
        document: Documento original (string)

    Returns:
        Documento con el nuevo valor
    """
    if document[0] == "3":
        generic_document = "30000000007"
    else:
        generic_document = "20222222223"
    return pad_left(generic_document, 20)


def detect_and_prepare_error_documents(
    merged_books: dict, book_key: str, field_number: int = 7
):
    """
    Extracts document IDs from the merged book data, checks for errors via AFIP,
    and maps those with errors to replacement-ready format.

    Args:
        merged_books (dict): Merged dictionary of both books.
        book_key (str): Identifier of the book to extract documents from.
        field_number (int): Field containing the document value (default 7).

    Returns:
        list: Tuples of (line_index, original_doc, new_doc) for erroneous documents.
    """
    extracted_docs = extract_document_ids(merged_books, book_key, field_number)
    error_docs = detect_invalid_documents(extracted_docs)
    return build_replacement_entries(extracted_docs, error_docs)


def build_replacement_entries(document_list, error_documents_strings):
    """
    Crea una lista de tuplas que contienen el índice y el documento
    para cada documento que aparece en la lista de documentos con errores.

    Args:
        document_list: Lista completa de documentos (enteros)
        error_documents_strings: Lista de documentos con errores (strings)

    Returns:
        Lista de tuplas (índice, documento) para documentos con errores
    """
    # Convertir error_documents a un conjunto de enteros para búsqueda eficiente
    error_docs_set = set(int(doc) for doc in error_documents_strings)

    indexed_error_documents = []
    for index, doc in enumerate(document_list):
        if doc in error_docs_set:
            index += 1  # Ajustar el índice para que sea 1-based
            original_doc = pad_left(str(doc), 20)
            new_doc = get_replacement_document_id(str(doc))
            # Agregar el índice y el documento a la lista
            indexed_error_documents.append((index, new_doc, original_doc))

    return indexed_error_documents
