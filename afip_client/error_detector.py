import os

from dotenv import load_dotenv

from afip_client.afip_service import AFIPService
from afip_client.error_utils import INSCRIPTION_ERROR_KEYS, find_keys_with_error_msgs
from logger import logger

# Load environment variables from the .env file
load_dotenv()


def detect_invalid_documents(nit_list) -> list:
    """
    Main function that reads configuration, processes the data from AFIPService,
    accumulates errors, filters successful records, and returns a list of document IDs with errors.
    """
    if not nit_list:
        logger.warning("Empty document list received. Skipping error check.")
        return []

    try:
        # Read parameters from environment variables (or use default values if needed)
        username = os.getenv("AFIP_USERNAME")
        password = os.getenv("AFIP_PASSWORD")
        base_url = os.getenv("AFIP_BASE_URL")
        chunk_size = int(os.getenv("AFIP_CHUNK_SIZE"))
        max_calls = int(os.getenv("AFIP_MAX_CALLS"))
        pause_duration = int(os.getenv("AFIP_PAUSE_DURATION"))
        max_retries = int(os.getenv("AFIP_MAX_RETRIES"))
        retry_delay = int(os.getenv("AFIP_RETRY_DELAY"))
        services_available = os.getenv("AFIP_SERVICES_AVAILABLE", "").split(",")

        logger.info("Total NITs to consult: %d", len(nit_list))

        # Create AFIP service
        service = AFIPService(
            username=username,
            password=password,
            base_url=base_url,
            chunk_size=chunk_size,
            max_calls=max_calls,
            pause_duration=pause_duration,
            max_retries=max_retries,
            retry_delay=retry_delay,
            services_available=services_available,
        )

        # Fetch data
        fetched_data = service.fetch_service_data("inscription", nit_list)
        if not fetched_data:
            logger.warning("No data fetched from AFIP.")
            return []

        logger.info("Data fetched: %d records", len(fetched_data))

        # Accumulate and filter errors
        data_with_error = service.accumulate_errors_in_data(
            fetched_data, INSCRIPTION_ERROR_KEYS
        )
        logger.debug("Records with errors: %d", len(data_with_error))

        error_messages = [
            "No existe persona con ese Id",
            "La clave se encuentra inactiva",
        ]
        key_with_error_msg = find_keys_with_error_msgs(data_with_error, error_messages)

        logger.debug("Records with error messages: %s", key_with_error_msg)
        logger.info("Records with errors messages: %d", len(key_with_error_msg))
        logger.info("Process completed AFIP Client.")

        return key_with_error_msg

    except Exception as e:
        logger.error("Error during document error identification: %s", str(e))
        return []
