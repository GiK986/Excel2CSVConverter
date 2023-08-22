import datetime
import os
import shutil

from dotenv import load_dotenv

from logger import Logger

load_dotenv()

INPUT_FOLDER = os.path.abspath(os.getenv("INPUT_FOLDER"))
OUTPUT_FOLDER = os.path.abspath(os.getenv("OUTPUT_FOLDER"))
LOG_FOLDER = os.path.abspath(os.getenv("LOG_FOLDER"))


def get_input_root_folder():
    date_now = datetime.datetime.now().strftime("%d.%m.%Y")
    return os.path.join(INPUT_FOLDER, date_now)


def get_log_file():
    ensure_directory_exists(LOG_FOLDER)
    date_now = datetime.datetime.now().strftime("%d.%m.%Y")
    path = os.path.join(LOG_FOLDER, date_now) + ".log"

    return path


def get_csv_path(excel_path):
    path = (os.path.splitext(excel_path)[0] + ".csv").replace(INPUT_FOLDER, OUTPUT_FOLDER)
    ensure_directory_exists(os.path.dirname(path))
    return path


def is_allowed_folder(path):
    return os.path.basename(os.path.normpath(path)).lower() not in ["010", "026"]


def ensure_directory_exists(directory):
    if not os.path.exists(directory):
        os.makedirs(directory)


def get_server_name():
    return os.getenv("SERVER_NAME")


def get_database_name():
    return os.getenv("DATABASE_NAME")


def get_database_user():
    return os.getenv("DATABASE_USER")


def get_database_password():
    return os.getenv("DATABASE_PASSWORD")


logger = Logger(log_file=get_log_file())


def remove_old_folders(directory, days_to_keep=7):
    today = datetime.datetime.now()
    for item in os.listdir(directory):
        item_path = os.path.join(directory, item)
        if os.path.isdir(item_path):
            modified_time = datetime.datetime.fromtimestamp(os.path.getmtime(item_path))
            age = (today - modified_time).days
            if age > days_to_keep:
                shutil.rmtree(item_path)
                logger.info(f"Removed old folder: {item_path}")


def remove_old_files(directory, days_to_keep=7):
    today = datetime.datetime.now()
    for item in os.listdir(directory):
        item_path = os.path.join(directory, item)
        if os.path.isfile(item_path):
            modified_time = datetime.datetime.fromtimestamp(os.path.getmtime(item_path))
            age = (today - modified_time).days
            if age > days_to_keep:
                os.remove(item_path)
                logger.info(f"Removed old file: {item_path}")


def remove_old_output_folders():
    remove_old_folders(OUTPUT_FOLDER)


def remove_old_log_files():
    remove_old_files(LOG_FOLDER)
