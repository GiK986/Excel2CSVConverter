import os

import pandas as pd

import utils
import validators
from logger import Logger

logger = Logger(log_file=utils.get_log_file())


def convert_excel_to_csv(excel_path, csv_path):
    logger.info(f"Processing: {excel_path}")
    try:
        df = pd.read_excel(excel_path, engine="openpyxl")
    except Exception as e:
        message = f"Error: converting {excel_path} to {csv_path}: {e}"
        logger.error(message)
        return

    duplicate_rows = validators.find_duplicate_first_column_rows(df)

    if not duplicate_rows.empty:
        validators.log_duplicate_rows(duplicate_rows)
        df_row_count_before = df.shape[0]
        df = df.drop_duplicates(subset=df.columns[0], keep="first")
        df_row_count_after = df.shape[0]
        duplicate_row_count = duplicate_rows.shape[0]
        removed_row_count = df_row_count_before - df_row_count_after
        message = f"Found {duplicate_row_count} duplicate rows. Removed {removed_row_count} of them."
        logger.warning(message)

    special_rows = validators.find_special_second_column_rows(df)

    if not special_rows.empty:
        validators.log_special_rows(special_rows)
        df = df.drop(special_rows.index)
        special_row_count = special_rows.shape[0]
        message = f"Found {special_row_count} rows where the second column is 0, NaN or empty string. Removed {special_row_count} of them."
        logger.warning(message)

    not_existing_items = validators.find_nonexistent_items(df)

    if not not_existing_items.empty:
        validators.log_nonexistent_items(not_existing_items)
        df = df.drop(not_existing_items.index)
        not_existing_item_count = not_existing_items.shape[0]
        message = f"Found {not_existing_item_count} nonexistent items. Removed {not_existing_item_count} of them."
        logger.warning(message)

    if df.empty:
        message = f"The file: {excel_path} is empty after validation"
        logger.error(message)
        return

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

    # Remove old folders and files
    utils.remove_old_output_folders()
    utils.remove_old_log_files()

    # Log a completion message
    logger.info("Excel to CSV conversion completed")
