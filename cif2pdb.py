import os
import argparse
from Bio import PDB

def convert_cifs_to_pdbs(input_dir, output_dir):
    os.makedirs(output_dir, exist_ok=True)
    
    parser = PDB.MMCIFParser(QUIET=True)
    writer = PDB.PDBIO()

    for filename in os.listdir(input_dir):
        if filename.endswith(".cif"):
            cif_path = os.path.join(input_dir, filename)
            pdb_id = os.path.splitext(filename)[0]
            pdb_path = os.path.join(output_dir, f"{pdb_id}.pdb")

            try:
                structure = parser.get_structure(pdb_id, cif_path)
                writer.set_structure(structure)
                writer.save(pdb_path)
                print(f"✅ Converted {filename} → {pdb_id}.pdb")
            except Exception as e:
                print(f"❌ Failed to convert {filename}: {e}")

if __name__ == "__main__":
    arg_parser = argparse.ArgumentParser(description="Convert CIF files to PDB format")
    arg_parser.add_argument("-input", required=True, help="Path to folder containing .cif files")
    arg_parser.add_argument("-output", required=True, help="Path to save .pdb files")

    args = arg_parser.parse_args()
    convert_cifs_to_pdbs(args.input, args.output)
