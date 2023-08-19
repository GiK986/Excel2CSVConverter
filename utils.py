import os
import datetime
from dotenv import load_dotenv

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
