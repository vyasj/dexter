import logging


def setup_logging(log_number):
    logging.basicConfig(
        level=logging.DEBUG,
        format='%(asctime)s - %(levelname)s - %(message)s',
        filename=f'logging/run_{log_number}.log',
        filemode='a'
    )


if __name__ == "__main__":
    pass