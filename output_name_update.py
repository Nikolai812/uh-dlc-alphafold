import argparse
import os
from typing import List

def get_sequences_names(job_folder: str, path: str = ".") -> List[str]:
    """
    Returns the list of first-level subfolders (sequence names) inside job_folder.
    Prints a warning if files are found at the first level.

    :param job_folder: Name of the job folder to check.
    :param path: Path to the directory containing job_folder (default: current directory).
    :return: List of subfolder names.
    """
    full_path = os.path.join(path, job_folder)

    if not os.path.isdir(full_path):
        raise NotADirectoryError(f"{full_path} is not a valid directory.")

    entries = os.listdir(full_path)
    subfolders = []
    files = []

    for entry in entries:
        entry_path = os.path.join(full_path, entry)
        if os.path.isdir(entry_path):
            subfolders.append(entry)
        elif os.path.isfile(entry_path):
            files.append(entry)

    if files:
        print(f"Warning: The following files were found in {full_path}: {', '.join(files)}")

    return subfolders


def include_sequence_name_into_output_filenames(job_folder: str, path: str = "."):
    """
    Renames files in each sequence subfolder by prefixing them with the subfolder (sequence) name.

    Example:
        old_name: result.pdb
        new_name: Seq1_result.pdb

    :param job_folder: Name of the main job folder containing sequence subfolders.
    :param path: Path to the directory containing job_folder (default: current directory).
    """
    # Import the helper defined earlier
    sequences = get_sequences_names(job_folder, path)

    full_job_path = os.path.join(path, job_folder)

    for seq_name in sequences:
        seq_path = os.path.join(full_job_path, seq_name)

        for entry in os.listdir(seq_path):
            entry_path = os.path.join(seq_path, entry)

            # Skip subfolders, only process files
            if os.path.isfile(entry_path):
                new_name = f"{seq_name}_{entry}"
                new_path = os.path.join(seq_path, new_name)

                # Only rename if not already renamed
                if not entry.startswith(f"{seq_name}_"):
                    os.rename(entry_path, new_path)
                    print(f"Renamed: {entry} → {new_name}")
                else:
                    print(f"Skipped (already renamed): {entry}")


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("-i", "--input_folder", dest="input_folder",
                        help="input jobnumber folder",
                        default="000000")

    parser.add_argument("-p", "--path", dest="folder_path",
                        help="jobnumber folder path",
                        default=".")

    args = parser.parse_args()
    input_folder = args.input_folder
    folder_path = args.folder_path

    include_sequence_name_into_output_filenames(job_folder=input_folder, path=folder_path)


