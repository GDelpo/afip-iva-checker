# afip-iva-checker

<p>
  <img alt="Python" src="https://img.shields.io/badge/python-3.9%2B-blue?logo=python&logoColor=white">
  <img alt="License" src="https://img.shields.io/badge/license-MIT-green">
  <img alt="Status" src="https://img.shields.io/badge/status-stable-green">
</p>

> Procesa libros IVA Ventas/Compras, valida formato, calcula totales y detecta discrepancias con AFIP. CLI + GUI.

## Features

- Parser modular de libros IVA Ventas/Compras en `core/`: validación de formato, totales, comparación cruzada.
- Cliente HTTP a AFIP `inscription` y `padron` con retries y limpieza de respuestas.
- CLI (`orchestrator.py`) y GUI Tkinter (`ui.py`).
- Reportes automáticos con diferencias vs los registros AFIP.
- Logging estructurado diario (`logs/afip_iva_checker_YYYYMMDD.log`).

## Requirements

- Python 3.9+
- Credenciales válidas para los servicios AFIP `inscription`/`padron`.

## Quickstart

### Install

```bash
git clone https://github.com/GDelpo/afip-iva-checker.git
cd afip-iva-checker
python -m venv env
source env/bin/activate          # Linux/macOS
# .\env\Scripts\Activate.ps1     # Windows
pip install -r requirements.txt
```

### Configure

```bash
cp .env.example .env
# Editar .env con credenciales AFIP
```

### Run — CLI

```bash
python orchestrator.py --input libros_iva.xlsx --output reporte.xlsx
```

### Run — GUI

```bash
python ui.py
```

## Configuration

Ver `.env.example` para la lista completa. Variables principales:

| Variable | Descripción |
|----------|-------------|
| `AFIP_API_URL` | URL del servicio AFIP (testing o prod) |
| `AFIP_API_USER` | Usuario |
| `AFIP_API_PASSWORD` | Password |
| `LOG_LEVEL` | `DEBUG` / `INFO` / `WARNING` |

## Architecture

```
afip-iva-checker/
├── orchestrator.py          # CLI entrypoint
├── ui.py                    # GUI Tkinter
├── logger.py                # Logging setup
├── afip_client/             # HTTP client
│   ├── afip_service.py
│   ├── error_detector.py
│   └── error_utils.py
├── core/                    # Business logic
│   ├── book_parser.py
│   ├── book_merger.py
│   ├── diff_formatter.py
│   ├── field_calculator.py
│   ├── report_generator.py
│   └── ...
└── models/                  # Data structures
```

**Stack:** `pandas` + `openpyxl` para Excel, `requests` para HTTP, Tkinter para GUI.

## License

[MIT](LICENSE) © 2026 Guido Delponte
