import pandas as pd

import utils
from logger import Logger

logger = Logger(log_file=utils.get_log_file())


def find_duplicate_first_column_rows(df):
    """Returns rows where the first column is duplicated"""
    first_col = df.iloc[:, 0]  # Assuming the first column is at index 0
    duplicate_mask = first_col.duplicated(keep=False)
    return df[duplicate_mask]


def log_duplicate_rows(df):
    logger.warning("Duplicate rows: \n" + df.to_string(index=True))


def find_special_second_column_rows(df):
    """Returns rows where the second column is 0, NaN or empty string"""
    second_col = df.iloc[:, 1]  # Assuming the second column is at index 1
    special_mask = (second_col == 0) | (pd.to_numeric(second_col, errors="coerce").isna()) | (second_col == "")
    return df[special_mask]


def log_special_rows(df):
    logger.warning("Rows with special second column values: \n" + df.to_string(index=True))
