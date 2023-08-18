import datetime
import os

import pandas as pd
from dotenv import load_dotenv

from logger import Logger

load_dotenv()

INPUT_FOLDER = os.path.abspath(os.getenv("INPUT_FOLDER"))
OUTPUT_FOLDER = os.path.abspath(os.getenv("OUTPUT_FOLDER"))
LOG_FOLDER = os.path.abspath(os.getenv("LOG_FOLDER"))


def get_input_root_folder():
    date_now = datetime.datetime.now().strftime("%d.%m.%Y")
    return os.path.join(INPUT_FOLDER, date_now)


def get_output_root_folder():
    date_now = datetime.datetime.now().strftime("%d.%m.%Y")
    return os.path.join(OUTPUT_FOLDER, date_now)


def get_log_file():
    if not os.path.exists(LOG_FOLDER):
        os.makedirs(LOG_FOLDER)
    date_now = datetime.datetime.now().strftime("%d.%m.%Y")
    path = os.path.join(LOG_FOLDER, date_now) + ".log"

    return path


logger = Logger(log_file=get_log_file())


def convert_excel_to_csv(excel_path, csv_path):
    try:
        df = pd.read_excel(excel_path, engine="openpyxl")
        df.to_csv(csv_path, index=False, sep=";")
    except Exception as e:
        logger.error(f"Error: converting {excel_path} to {csv_path}: {e}")


def get_csv_path(excel_path):
    path = (os.path.splitext(excel_path)[0] + ".csv").replace(INPUT_FOLDER, OUTPUT_FOLDER)

    if not os.path.exists(os.path.dirname(path)):
        os.makedirs(os.path.dirname(path))

    return path


def get_last_dirname(path):
    return os.path.basename(os.path.normpath(path))


def convert_folder_contents(input_folder):
    for root, _, files in os.walk(input_folder):
        for file in files:
            if file.lower().endswith(".xlsx") \
                    and get_last_dirname(root).lower() not in ["010", "026"]:
                excel_path = os.path.join(root, file)
                csv_path = get_csv_path(excel_path)
                convert_excel_to_csv(excel_path, csv_path)
                logger.info(f"Converted: {excel_path} -> {csv_path}")


if __name__ == "__main__":
    input_root_folder = get_input_root_folder()
    if not os.path.exists(input_root_folder):
        logger.info(f"Input folder not found: {input_root_folder}")
        exit(0)

    convert_folder_contents(input_root_folder)
    # Log a completion message
    logger.info("Excel to CSV conversion completed")
