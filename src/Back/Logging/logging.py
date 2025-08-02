import logging

def setup_logger(name, log_file='backend.log', level=logging.INFO):
    """Configure and return a logger for backend components.
    
    Args:
        name (str): Name of the logger.
        log_file (str): Path to the log file. Defaults to 'backend.log'.
        level: Logging level (e.g., logging.INFO, logging.ERROR).
    
    Returns:
        logging.Logger: Configured logger instance.
    """
    logger = logging.getLogger(name)
    if not logger.handlers:  # Avoid duplicate handlers
        logger.setLevel(level)
        handler = logging.FileHandler(log_file)
        formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        handler.setFormatter(formatter)
        logger.addHandler(handler)
    return logger

def log_exception(logger, exception, message):
    """Log an exception with additional context.
    
    Args:
        logger (logging.Logger): Logger instance to use.
        exception (Exception): The exception to log.
        message (str): Additional message to include in the log.
    """
    logger.error(f"{message}: {str(exception)}", exc_info=True)
