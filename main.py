"""
1. Написать приложение на python, которое умеет реплицировать данные из директории.
2. Приложение должно иметь возможность выбрать реплицируемую директорию и целевой путь для реплики.
3. Приложение необходимо покрыть функциональными тестами с использованием pytest

Ограничения:
Не использовать в реализации готовые сервисы или библиотеки реализующие функциональность репликации данных.
Любые другие библиотеки использовать можно.
"""
import argparse

from logger import logger
from replication import replicate_directory


def main() -> None:
    parser = argparse.ArgumentParser(description="Directory replication.")
    parser.add_argument("reference_directory", help="Path to the reference directory.")
    parser.add_argument("target_directory", help="Path to the target directory.")
    args = parser.parse_args()

    try:
        replicate_directory(args.reference_directory, args.target_directory)
        logger.info(f"{args.reference_directory} directory has been successfully replicated to {args.target_directory}")
    except Exception as e:
        logger.error(f"Error: {e}")


if __name__ == "__main__":
    main()
