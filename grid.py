#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Processes specific '*_model.cif' files found directly within the first-level
subdirectories of a specified input directory using PyMOL. It arranges them
in a grid view, saves a PNG snapshot, and saves a PyMOL session file (.pse)
within the input directory by default.
"""

import os
import argparse
import pymol
from pymol import cmd
import sys # For sys.exit

def create_pymol_grid(input_dir, output_image, output_session):
    """
    Generates a grid view of proteins from specific .cif files using PyMOL.

    Args:
        input_dir (str): The parent directory containing subfolders with .cif files.
        output_image (str): The full path to save the output PNG image.
        output_session (str): The full path to save the output PyMOL session (.pse) file.
    """
    # --- Argument Validation ---
    if not os.path.isdir(input_dir):
        print(f"Error: Input directory '{input_dir}' not found or is not a directory.")
        sys.exit(1) # Exit with error status

    # --- Start PyMOL ---
    try:
        pymol.finish_launching(['pymol', '-qc'])
    except Exception as e:
        print(f"Error launching PyMOL: {e}")
        print("Make sure PyMOL is installed and accessible in your environment.")
        sys.exit(1)

    # --- File Collection (One Level Deep) ---
    all_cif_files = []
    print(f"Searching for '*_model.cif' files in immediate subdirectories of '{input_dir}'...")

    try:
        # List items directly inside input_dir
        for item_name in os.listdir(input_dir):
            item_path = os.path.join(input_dir, item_name)

            # Check if the item is a directory
            if os.path.isdir(item_path):
                # Construct the expected specific CIF file path within this subdirectory
                # Assumes the CIF file name matches the subdirectory name + "_model.cif"
                expected_cif_filename = f"{item_name}_model.cif"
                cif_file_path = os.path.join(item_path, expected_cif_filename)

                # Check if this specific file exists
                if os.path.isfile(cif_file_path):
                    all_cif_files.append(cif_file_path)
                    print(f"  Found: {cif_file_path}")

    except OSError as e:
        print(f"Error accessing directory '{input_dir}': {e}")
        sys.exit(1)


    # --- Processing ---
    if not all_cif_files:
        print("No matching '*_model.cif' files found in the immediate subdirectories.")
    else:
        print(f"Found {len(all_cif_files)} matching '.cif' files. Processing...")
        cmd.delete("all") # Clear any pre-existing objects in PyMOL

        # Set up PyMOL grid and background
        cmd.bg_color("white")
        cmd.set("grid_mode", 1)

        # Load all collected .cif files
        loaded_count = 0
        for cif_file in all_cif_files:
            try:
                # Use the directory name as the base for the PyMOL object name
                protein_dir_name = os.path.basename(os.path.dirname(cif_file))
                # Sanitize name for PyMOL
                protein_name = "".join(c if c.isalnum() else "_" for c in protein_dir_name)
                if not protein_name:
                    protein_name = f"protein_{loaded_count + 1}"

                # Ensure unique name
                unique_protein_name = protein_name
                counter = 1
                while unique_protein_name in cmd.get_names("objects"):
                    unique_protein_name = f"{protein_name}_{counter}"
                    counter += 1

                print(f"  Loading: {os.path.basename(cif_file)} as {unique_protein_name}")
                cmd.load(cif_file, unique_protein_name)

                # Add labels using the original directory name for clarity
                cmd.label(f"{unique_protein_name} and name CA", f'"{protein_dir_name}"')
                loaded_count += 1
            except Exception as e:
                print(f"  Warning: Failed to load or process {cif_file}: {e}")

        if loaded_count > 0:
            # Arrange structures
            print("Arranging structures in grid...")
            cmd.orient()
            cmd.show_as("cartoon")
            cmd.zoom()
            cmd.util.cnc() # Center view

            # --- Output Saving ---
            try:
                print(f"Saving grid snapshot to {output_image}...")
                # Ensure parent directory for output image exists (if specified elsewhere)
                os.makedirs(os.path.dirname(output_image), exist_ok=True)
                cmd.png(output_image, width=8000, height=8000, dpi=300, ray=1)
                print(f"Grid snapshot saved successfully.")
            except Exception as e:
                print(f"Error saving PNG image '{output_image}': {e}")

            try:
                print(f"Saving grid session file to {output_session}...")
                 # Ensure parent directory for output session exists (if specified elsewhere)
                os.makedirs(os.path.dirname(output_session), exist_ok=True)
                cmd.save(output_session)
                print(f"Grid session file saved successfully.")
            except Exception as e:
                print(f"Error saving PSE session '{output_session}': {e}")

            # --- Cleanup ---
            cmd.delete("all")
        else:
            print("No structures were successfully loaded.")

    # --- Shutdown PyMOL ---
    # cmd.quit() # Consider uncommenting if running many instances sequentially

    print("Processing complete!")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Create a PyMOL grid view from '*_model.cif' files found in the immediate subdirectories of the input directory.",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter
    )

    parser.add_argument(
        "-i", "--input_dir",
        required=True,
        help="Parent directory containing subfolders. Script will look for '<subdir_name>_model.cif' inside each subfolder."
    )
    parser.add_argument(
        "-img", "--output_image",
        default=None,
        help="Full path for the output PNG image file. "
             "If not provided, defaults to 'protein_grid_view.png' inside the --input_dir."
    )
    parser.add_argument(
        "-pse", "--output_session",
        default=None,
        help="Full path for the output PyMOL session (.pse) file. "
             "If not provided, defaults to 'protein_grid_view.pse' inside the --input_dir."
    )

    args = parser.parse_args()

    # --- Determine Output Paths (Defaulting to inside input_dir) ---
    if args.output_image is None:
        # Default PNG path inside the input directory
        output_image_path = os.path.join(args.input_dir, "protein_grid_view.png")
    else:
        output_image_path = args.output_image

    if args.output_session is None:
        # Default PSE path inside the input directory
        output_session_path = os.path.join(args.input_dir, "protein_grid_view.pse")
    else:
        output_session_path = args.output_session

    # --- Run the main function ---
    create_pymol_grid(args.input_dir, output_image_path, output_session_path)
