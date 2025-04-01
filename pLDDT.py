import os
import json
import argparse
import csv

def calculate_plddt_scores(folder_path):
    """
    Calculate average pLDDT scores and create output files.

    Args:
        folder_path (str): Path to the main directory containing subfolders.
    """
    # Dictionary to store average pLDDT scores
    average_plddt_scores = {}

    # Traverse through subfolders
    for folder_name in os.listdir(folder_path):
        folder_full_path = os.path.join(folder_path, folder_name)
        if os.path.isdir(folder_full_path):
            # Look for the <job_name>_confidences.json file
            for file_name in os.listdir(folder_full_path):
                if file_name.endswith("_confidences.json"):
                    file_path = os.path.join(folder_full_path, file_name)

                    # Open and parse the JSON file
                    with open(file_path, "r") as json_file:
                        data = json.load(json_file)
                        # Extract atom_plddts and calculate the average
                        if "atom_plddts" in data:
                            atom_plddts = data["atom_plddts"]
                            average_plddt = sum(atom_plddts) / len(atom_plddts) if atom_plddts else 0
                            average_plddt_scores[folder_name] = average_plddt

                            # Create a text file in the subfolder with the score
                            output_file_name = f"{folder_name}_pLDDT_{average_plddt:.2f}.txt"
                            output_file_path = os.path.join(folder_full_path, output_file_name)
                            with open(output_file_path, "w") as output_file:
                                output_file.write(f"Average pLDDT Score: {average_plddt:.2f}\n")

    # Write all scores to a CSV file in the main folder
    csv_file_path = os.path.join(folder_path, "average_plddt_scores.csv")
    with open(csv_file_path, "w", newline="") as csv_file:
        csv_writer = csv.writer(csv_file)
        csv_writer.writerow(["Subfolder", "Average pLDDT"])
        for folder, avg_plddt in average_plddt_scores.items():
            csv_writer.writerow([folder, f"{avg_plddt:.2f}"])

    print(f"Average pLDDT scores written to {csv_file_path}")

if __name__ == "__main__":
    # Argument parser setup
    parser = argparse.ArgumentParser(description="Calculate average pLDDT scores for AlphaFold subfolders.")
    parser.add_argument("folder_path", type=str, help="Path to the main folder containing AlphaFold outputs.")

    args = parser.parse_args()

    # Calculate pLDDT scores
    calculate_plddt_scores(args.folder_path)
