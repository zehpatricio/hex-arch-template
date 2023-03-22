import dataset


def check_database(db_url: str) -> bool:
    """
    Check if the database is up and running by executing a simple SQL query.

    Args:
        db_url (str): The database URL.

    Returns:
        bool: True if the database is up and running, False otherwise.
    """
    try:
        database = dataset.connect(db_url)
        database.query("SELECT 1")
        return True
    except:
        return False
