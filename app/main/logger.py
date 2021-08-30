import logging


def setup_logging(name="logger",
                  filepath=None,
                  stream_log_level="DEBUG",
                  file_log_level="DEBUG"):
    logger = logging.getLogger(name)
    logger.setLevel("DEBUG")
    formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s:'
    )
    logging.StreamHandler(stream=None)
    if filepath is not None:
        fh = logging.FileHandler(filepath)
        fh.setLevel(getattr(logging, file_log_level))
        fh.setFormatter(formatter)
        logger.addHandler(fh)
    return logger


def log_decorator(log_name):
    def log_this(function):
        logger = logging.getLogger(log_name)

        def new_function(*args, **kwargs):
            logger.debug(f"{function.__name__} - {args} - {kwargs}")
            output = function(*args, **kwargs)
            out = [post['text'] for post in output]
            logger.debug(f"{function.__name__} returned: {out}")
            return output
        return new_function
    return log_this


logger = setup_logging(name="default_log", filepath="log_file.log")
