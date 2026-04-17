class ProcessingError(Exception):
    """Excepción personalizada para errores durante el procesamiento de libros."""

    def __init__(self, message):
        super().__init__(message)
        self.message = message
