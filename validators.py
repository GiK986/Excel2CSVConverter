from logger import Logger
import utils


logger = Logger(log_file=utils.get_log_file())


def find_duplicate_first_column_rows(df):
    first_col = df.iloc[:, 0]  # Assuming the first column is at index 0
    duplicate_mask = first_col.duplicated(keep=False)
    return df[duplicate_mask]


def log_duplicate_rows(df):
    logger.info("Duplicate rows: \n" + df.to_string(index=True))