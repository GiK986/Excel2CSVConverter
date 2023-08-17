import datetime
import os
import pandas as pd
from dotenv import load_dotenv

load_dotenv()

INPUT_FOLDER = os.path.abspath(os.getenv("INPUT_FOLDER"))
OUTPUT_FOLDER = os.path.abspath(os.getenv("OUTPUT_FOLDER"))


def get_input_root_folder():
    date_now = datetime.datetime.now().strftime("%d.%m.%Y")
    return os.path.join(INPUT_FOLDER, date_now)


def get_output_root_folder():
    date_now = datetime.datetime.now().strftime("%d.%m.%Y")
    return os.path.join(OUTPUT_FOLDER, date_now)


def convert_excel_to_csv(excel_path, csv_path):
    try:
        df = pd.read_excel(excel_path, engine="openpyxl")
        df.to_csv(csv_path, index=False)
    except Exception as e:
        print(f"Error converting {excel_path} to {csv_path}: {e}")


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
                print(f"Converted: {excel_path} -> {csv_path}")


if __name__ == "__main__":
    input_root_folder = get_input_root_folder()
    if not os.path.exists(input_root_folder):
        print(f"Input folder not found: {input_root_folder}")
        exit(0)

    convert_folder_contents(input_root_folder)
