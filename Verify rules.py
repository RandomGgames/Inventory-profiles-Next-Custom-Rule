import json
import logging
import os
import pathlib
import sys
import time
import toml
import traceback
import typing
from datetime import datetime

logger = logging.getLogger(__name__)


def read_text_file_lines(file_path: typing.Union[str, pathlib.Path]) -> typing.List[str]:
    """
    Reads a text file and returns a list of strings with the \n characters at the end of each line removed.
    Includes error checking and logging.

    Args:
    file_path (typing.Union[str, pathlib.Path]): The file path of the text file to read.

    Returns:
    typing.List[str]: A list of strings with the \n characters at the end of each line removed.
    """
    try:
        with open(file_path, 'r') as f:
            lines = [line.strip() for line in f]
        logger.info(f"Successfully read {file_path}")
        return lines
    except Exception as e:
        logger.error(f"Error reading {file_path}: {e}")
        return []


def main() -> None:
    item_ids_list_file_path = "Item IDs 1.21.9-1.21.10.txt"
    rules_file_path = "rules-v2.txt"

    item_ids = read_text_file_lines(item_ids_list_file_path)
    item_ids = {id.strip() for id in item_ids if id.strip()}
    # logger.debug(f'{item_ids=}')
    
    rules_item_ids = read_text_file_lines(rules_file_path)
    rules_item_ids = {id.strip() for id in rules_item_ids if id.strip()}
    # logger.debug(f'{rules_item_ids=}')
    
    missing_ids = []
    for id in item_ids:
        if id not in rules_item_ids:
            missing_ids.append(id)
    logger.debug(f'{missing_ids=}')

def setup_logging(
        logger: logging.Logger,
        log_file_path: typing.Union[str, pathlib.Path],
        console_logging_level: int = logging.DEBUG,
        file_logging_level: int = logging.DEBUG,
        log_message_format: str = "%(asctime)s.%(msecs)03d %(levelname)s [%(funcName)s] [%(name)s]: %(message)s",
        date_format: str = "%Y-%m-%d %H:%M:%S") -> None:
    logger.setLevel(file_logging_level)  # Set the overall logging level

    # File Handler for script-named log file (overwrite each run)
    file_handler = logging.FileHandler(log_file_path, encoding="utf-8", mode="w")
    file_handler.setLevel(file_logging_level)
    file_handler.setFormatter(logging.Formatter(log_message_format, datefmt=date_format))
    logger.addHandler(file_handler)

    # Console Handler
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setLevel(console_logging_level)
    console_handler.setFormatter(logging.Formatter(log_message_format, datefmt=date_format))
    logger.addHandler(console_handler)

    # Set specific logging levels if needed
    # logging.getLogger("requests").setLevel(logging.INFO)


if __name__ == "__main__":
    script_name = pathlib.Path(__file__).stem
    log_file_name = f"{script_name}.log"
    log_file_path = pathlib.Path(log_file_name)
    setup_logging(logger, log_file_path, log_message_format="%(asctime)s.%(msecs)03d %(levelname)s [%(funcName)s]: %(message)s")

    error = 0
    try:
        start_time = time.perf_counter()
        logger.info("Starting operation...")
        main()
        end_time = time.perf_counter()
        duration = end_time - start_time
        logger.debug(f"Completed operation in {duration:.4f}s.")
    except Exception as e:
        logger.warning(f"A fatal error has occurred: {repr(e)}\n{traceback.format_exc()}")
        error = 1
    finally:
        sys.exit(error)
