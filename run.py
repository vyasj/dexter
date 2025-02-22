import build_db
import dl_images
import argparse
import logging
import os


def setup_logging(log_number):
    logging.basicConfig(
        level=logging.DEBUG,
        format='%(asctime)s - %(levelname)s - %(message)s',
        filename=f'logging/dl_images_log_{log_number}.log',
        filemode='a'
    )


if __name__ == "__main__":

    parser = argparse.ArgumentParser()
    parser.add_argument("-c", "--create", help="Create database", action="store_true")
    parser.add_argument("-p", "--populate", help="Populate database", action="store_true")
    parser.add_argument("-d", "--dl_batch_size", help="Batch size for downloading images", default=None)

    args = parser.parse_args()

    
    logfile_count = len([item for item in os.listdir("logging/") if os.path.isfile(os.path.join("logging/", item))])
    setup_logging(logfile_count+1)
    
    if args.create:
        build_db.create()
    if args.populate:
        build_db.populate()
    
    if args.dl_batch_size is not None:
        dl_images.download(int(args.dl_batch_size))