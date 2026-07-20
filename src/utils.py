import os

import yaml


CURRENT_PATH = os.path.dirname(os.path.abspath(__file__))
CONFIG_PATH = os.path.abspath(os.path.join(CURRENT_PATH, "..", "config.yaml"))
RAW_DATA_PATH = os.path.abspath(os.path.join(CURRENT_PATH, "..", "raw_data"))
PROCESSED_DATA_PATH = os.path.abspath(os.path.join(CURRENT_PATH, "..", "processed_data"))


def read_config(config_path: str) -> dict:
    """
    Baca file config YAML dan return sebagai dictionary
    """
    try:
        with open(config_path, "r") as file:
            config = yaml.safe_load(file)
        
        print("Berhasil membaca config")
        return config
    
    except FileNotFoundError:
        print(f"Error: File tidak ditemukan di {config_path}")
        raise
    except yaml.YAMLError as exc:
        print(f"Error saat membaca file YAML: {exc}")
        raise

