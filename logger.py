import logging
import os
from datetime import datetime


def setup_logger(log_level=logging.INFO):
    """
    Configura el logger para el proyecto.

    Args:
        log_level: Nivel de log (por defecto INFO)

    Returns:
        Logger configurado
    """
    # Crear directorio de logs si no existe
    log_dir = "logs"
    if not os.path.exists(log_dir):
        os.makedirs(log_dir)

    # Configurar el logger
    logger = logging.getLogger("afip_iva_checker")
    logger.setLevel(log_level)

    # Evitar duplicación de handlers
    if not logger.handlers:
        # Handler para consola
        console_handler = logging.StreamHandler()
        console_handler.setLevel(log_level)
        console_format = logging.Formatter(
            "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
        )
        console_handler.setFormatter(console_format)

        # Handler para archivo
        log_file = (
            f"{log_dir}/afip_iva_checker_{datetime.now().strftime('%d-%m-%Y')}.log"
        )
        file_handler = logging.FileHandler(log_file, encoding="utf-8")
        file_handler.setLevel(log_level)
        file_format = logging.Formatter(
            "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
        )
        file_handler.setFormatter(file_format)

        # Agregar handlers al logger
        logger.addHandler(console_handler)
        logger.addHandler(file_handler)

    return logger


# Crear instancia global del logger
logger = setup_logger()
