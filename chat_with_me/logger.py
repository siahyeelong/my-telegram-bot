import logging
from colorama import Fore, Style, init

# Initialize colorama
init()

# Define color mappings
LOG_COLORS = {
    'DEBUG': Fore.BLUE + Style.BRIGHT,
    'INFO': Fore.GREEN + Style.BRIGHT,
    'WARNING': Fore.YELLOW + Style.BRIGHT,
    'ERROR': Fore.RED + Style.BRIGHT,
    'CRITICAL': Fore.RED + Style.BRIGHT,
}

class ColorFormatter(logging.Formatter):
    def format(self, record):
        log_color = LOG_COLORS.get(record.levelname, Fore.WHITE)
        log_message = super().format(record)
        return f"{log_color}{log_message}{Style.RESET_ALL}"

def setup_logger(name='colored_logger', level=logging.DEBUG):
    # Create a logger
    logger = logging.getLogger(name)
    logger.setLevel(level)  # Set the lowest level of logging

    # Create console handler and set level to debug
    ch = logging.StreamHandler()
    ch.setLevel(level)

    # Create formatter
    formatter = ColorFormatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')

    # Add formatter to ch
    ch.setFormatter(formatter)

    # Add ch to logger
    if not logger.handlers:
        logger.addHandler(ch)

    return logger
