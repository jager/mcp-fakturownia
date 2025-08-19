def filter_clients_by_name(clients: list, name: str) -> list:
    """Filter clients by name.

    Args:
        clients: A list of client dictionaries.
        name: The name to filter by.

    Returns:
        A list of clients that match the given name.
    """
    return [client for client in clients if name.lower() in client.get("name", "").lower()]