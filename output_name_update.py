import argparse
import os
import json
import shutil
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


def process_ranking_and_write_summary(job_folder: str, path: str = "."):
    job_path = os.path.join(path, job_folder)
    processed_folder = f"{job_folder}_processed"
    processed_path = os.path.join(path, processed_folder)

    # Create the processed folder if it doesn't exist
    os.makedirs(processed_path, exist_ok=True)

    # Dictionary to store best models and their values
    best_models_data = {}

    # Iterate over each subfolder in the job_folder
    for subfolder_name in os.listdir(job_path):
        subfolder_path = os.path.join(job_path, subfolder_name)

        # Check if it's a directory
        if not os.path.isdir(subfolder_path):
            continue

        # Try to read the ranking_debug.json file
        ranking_file = os.path.join(subfolder_path, f"{subfolder_name}_ranking_debug.json")
        if not os.path.exists(ranking_file):
            ranking_file = os.path.join(subfolder_path, "ranking_debug.json")
            if not os.path.exists(ranking_file):
                print(f"Ranking file not found in {subfolder_name}")
                continue

        # Read the ranking file
        with open(ranking_file, 'r') as f:
            ranking_data = json.load(f)

        # Get the first value from the "order" array
        best_model = ranking_data["order"][0]

        # Get the corresponding pLDDT value
        best_value = ranking_data["plddts"][best_model]

        # Add to the best_models_data dictionary
        best_models_data[f"{subfolder_name}_{best_model}"] = best_value

        # Find the corresponding PDB file
        pdb_file = os.path.join(subfolder_path, f"unrelaxed_{best_model}.pdb")
        if not os.path.exists(pdb_file):
            pdb_file = os.path.join(subfolder_path, f"{subfolder_name}_unrelaxed_{best_model}.pdb")
            if not os.path.exists(pdb_file):
                print(f"PDB file not found for {best_model} in {subfolder_name}")
                continue

        # Copy the PDB file to the processed directory with the new name
        new_pdb_name = f"{subfolder_name}_best_unrelaxed_model.pdb"
        new_pdb_path = os.path.join(processed_path, new_pdb_name)
        shutil.copy(pdb_file, new_pdb_path)
        print(f"Copied {pdb_file} to {new_pdb_path}")

    # Write the best_models_data to best_models.json in the processed folder
    best_models_file = os.path.join(processed_path, "best_models.json")
    with open(best_models_file, 'w') as f:
        json.dump(best_models_data, f, indent=4)
    print(f"Best models data written to {best_models_file}")


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

# Updating of the job output folder is postponed, probably not needed at all
#    include_sequence_name_into_output_filenames(job_folder=input_folder, path=folder_path)

# Here all output of the script is written to the newly created folder: old_name+processed
process_ranking_and_write_summary(input_folder, folder_path)


