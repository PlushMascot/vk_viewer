import logging


def setup_logging(name="logger",
                  filepath=None
                  ):
    logger = logging.getLogger(name)
    logger.setLevel(logging.DEBUG)
    formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )

    if filepath is not None:
        fh = logging.FileHandler(filepath)
        fh.setLevel(logging.DEBUG)
        fh.setFormatter(formatter)
        logger.addHandler(fh)

    return logger


def log_extraction(log_name):
    def log_this(function):
        logger = logging.getLogger(log_name)

        def new_function(*args, **kwargs):
            logger.debug(f"{function.__name__} - {args} - {kwargs}")
            output = function(*args, **kwargs)
            logger.debug(f"{function.__name__} returned {len(output)} posts")
            return output
        return new_function
    return log_this


logger = setup_logging(name="logger", filepath="log_file.log")
