import logging


LOGGER = logging.getLogger(__name__)


def hello(name: str) -> str:
    """Returns and prints a greeting

    Args:
        name: A name to greet

    Returns: The full greeting

    """
    greeting = f"Hello {name}"
    LOGGER.info(greeting)
    LOGGER.info(f"I said '{greeting}'.")
    return greeting
