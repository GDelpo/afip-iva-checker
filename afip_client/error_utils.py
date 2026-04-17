INSCRIPTION_ERROR_KEYS = ["errorMonotributo", "errorConstancia", "errorRegimenGeneral"]


def find_keys_with_error_msgs(dictionary, error_msgs):
    """
    Receives a dictionary and an error message (or a list of error messages),
    and returns a list of keys whose values (or any element within them, if they're lists)
    contain one or more of the error messages.

    Args:
        dictionary (dict): The dictionary with data.
        error_msgs (str or list): The error message or list of error messages to search for.

    Returns:
        list: A list of keys that contain at least one of the error messages.
    """
    # If error_msgs is not a list, convert it to a list
    if not isinstance(error_msgs, list):
        error_msgs = [error_msgs]

    keys_with_error = []

    for key, value in dictionary.items():
        if isinstance(value, list):
            for error_msg in error_msgs:
                if any(error_msg in item for item in value):
                    keys_with_error.append(key)
                    break  # Stop checking further messages for this key
        elif isinstance(value, str):
            for error_msg in error_msgs:
                if error_msg in value:
                    keys_with_error.append(key)
                    break  # Stop checking further messages for this key

    return keys_with_error
