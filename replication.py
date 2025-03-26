import filecmp
import os

from logger import logger


def copy_file(ref, targ) -> None:
    with open(ref, 'rb') as ref_file:
        data = ref_file.read()

    with open(targ, 'wb') as targ_file:
        targ_file.write(data)


def replicate_directory(reference_directory: str, target_directory: str) -> None:
    if not os.path.exists(reference_directory):
        raise Exception("Source directory not found")

    if not os.path.exists(target_directory):
        os.makedirs(target_directory)
        logger.info(f"Created target directory: {target_directory}")

    for reference_root, reference_dirs, reference_files in os.walk(reference_directory):
        path_to_reference = os.path.relpath(reference_root, reference_directory)
        target_root = os.path.join(target_directory, path_to_reference)

        if not os.path.exists(target_root):
            os.makedirs(target_root)
            logger.info(f"Created folder: {target_root}")

        for file in reference_files:
            reference_file = os.path.join(reference_root, file)
            target_file = os.path.join(target_root, file)

            if not os.path.exists(target_file) or not filecmp.cmp(reference_file, target_file, shallow=False):
                copy_file(reference_file, target_file)
                logger.info(f"Copied file: {reference_file} to {target_file}")

    for target_root, target_dirs, target_files in os.walk(target_directory, topdown=False):
        path_to_target = os.path.relpath(target_root, target_directory)
        reference_root = os.path.join(reference_directory, path_to_target)

        for file in target_files:
            target_file = os.path.join(target_root, file)
            reference_file = os.path.join(reference_root, file)

            if not os.path.exists(reference_file):
                os.remove(target_file)
                logger.info(f"Deleted file: {target_file}")

        if not os.path.exists(reference_root):
            os.rmdir(target_root)
            logger.info(f"Deleted folder: {target_root}")

    logger.info("Replication completed!")
