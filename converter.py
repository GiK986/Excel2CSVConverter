import os

import pandas as pd

import utils
import validators
from logger import Logger

logger = Logger(log_file=utils.get_log_file())


def convert_excel_to_csv(excel_path, csv_path):
    try:
        df = pd.read_excel(excel_path, engine="openpyxl")
    except Exception as e:
        message = f"Error: converting {excel_path} to {csv_path}: {e}"
        logger.error(message)
        return

    duplicate_rows = validators.find_duplicate_first_column_rows(df)

    if not duplicate_rows.empty:
        validators.log_duplicate_rows(duplicate_rows)
        df = df.drop_duplicates(subset=df.columns[0], keep="first")
        message = "Duplicate rows found. Removed duplicates."
        logger.info(message)

    df.to_csv(csv_path, index=False, sep=";")
    message = f"Converted: {excel_path} -> {csv_path}"
    logger.info(message)


def convert_folder_contents(input_folder):
    for root, _, files in os.walk(input_folder):
        for file in files:
            if file.lower().endswith(".xlsx") \
                    and utils.is_allowed_folder(root):
                excel_path = os.path.join(root, file)
                csv_path = utils.get_csv_path(excel_path)
                convert_excel_to_csv(excel_path, csv_path)


if __name__ == "__main__":
    input_root_folder = utils.get_input_root_folder()
    if not os.path.exists(input_root_folder):
        logger.info(f"Input folder not found: {input_root_folder}")
        exit(0)

    convert_folder_contents(input_root_folder)
    # Log a completion message
    logger.info("Excel to CSV conversion completed")
