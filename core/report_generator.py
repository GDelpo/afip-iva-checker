import json
import os
from datetime import datetime
from typing import Any, Dict, List, Tuple

from core.exceptions import ProcessingError
from logger import logger


def generate_final_report(
    processed_data: Dict[str, Any],
    difference_tuples: List[Tuple[int, Any, Any]],
    output_dir: str = None,
    include_summary: bool = True,
) -> str:
    """
    Genera un reporte final en formato JSON con:
      - Fecha y hora de ejecución.
      - (Opcional) Resumen de datos procesados.
      - Discrepancias encontradas (si las hay).

    Args:
        processed_data: Diccionario con los datos fusionados y procesados.
        difference_tuples: Lista de tuplas (línea, valor_correcto, valor_actual).
        output_dir: Carpeta donde guardar el reporte. Si es None, usa el directorio actual.
        include_summary: Si es True, incluye conteo y datos procesados; si False, sólo diferencias.

    Returns:
        Ruta al archivo JSON generado.
    """
    try:
        # Establecer carpeta de salida
        base_dir = output_dir or os.getcwd()
        os.makedirs(base_dir, exist_ok=True)
        msg = "Resumen del procesamiento:"
        # Construir estructura de reporte
        report: Dict[str, Any] = {
            "query_date": datetime.now().strftime("%d/%m/%Y %H:%M:%S"),
        }
        if include_summary:
            report["processed_data"] = {
                "total_records": len(processed_data),
                "data": processed_data,
            }
            msg += f"\nDatos procesados: {len(processed_data)}"

        # Agregar diferencias
        if difference_tuples:
            diffs = {
                line: {"correct_value": correct, "actual_value": actual}
                for line, correct, actual in difference_tuples
            }
            report["differences"] = {
                "total": len(difference_tuples),
                "entries": diffs,
            }
            msg += f"\nDiferencias encontradas: {len(difference_tuples)}"
        else:
            report["differences"] = {"total": 0, "entries": {}}

        # Nombre de archivo por fecha
        filename = f"final_report_{datetime.now().strftime('%Y-%m-%d_%H%M%S')}.json"
        file_path = os.path.join(base_dir, filename)
        msg += f"\nRuta del archivo: {file_path.replace(os.sep, '/')}"

        # Guardar JSON
        with open(file_path, "w", encoding="utf-8") as f:
            json.dump(report, f, ensure_ascii=False, indent=2)

        logger.info(f"Reporte generado en {file_path}")
        return msg

    except Exception as e:
        logger.exception("Error generando reporte final")
        raise ProcessingError(f"Error generando reporte: {e}") from e
