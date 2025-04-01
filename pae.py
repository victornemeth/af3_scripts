import os
import json
import argparse
import matplotlib.pyplot as plt
import numpy as np

def generate_pae_heatmaps(folder_path):
    """
    Generate PAE heatmaps for each subfolder using values from <job_name>_confidences.json.

    Args:
        folder_path (str): Path to the main directory containing subfolders.
    """
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

                        # Check if "pae" exists in the JSON
                        if "pae" in data:
                            pae_values = np.array(data["pae"])

                            # Create the heatmap
                            plt.figure(figsize=(8, 8))
                            plt.imshow(pae_values, cmap="Greens_r", interpolation="nearest")
                            plt.colorbar(label="Expected Position Error (Ångströms)")
                            plt.title(f"PAE Heatmap - {folder_name}")
                            plt.xlabel("Scored Residue")
                            plt.ylabel("Aligned Residue")

                            # Save the heatmap as an image
                            heatmap_path = os.path.join(folder_full_path, f"{folder_name}_pae_heatmap.png")
                            plt.savefig(heatmap_path, dpi=300, bbox_inches="tight")
                            plt.close()

                            print(f"Heatmap saved for {folder_name} at {heatmap_path}")

if __name__ == "__main__":
    # Argument parser setup
    parser = argparse.ArgumentParser(description="Generate PAE heatmaps for AlphaFold subfolders.")
    parser.add_argument("folder_path", type=str, help="Path to the main folder containing AlphaFold outputs.")

    args = parser.parse_args()

    # Generate PAE heatmaps
    generate_pae_heatmaps(args.folder_path)
