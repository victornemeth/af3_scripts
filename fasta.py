import os
import json
import argparse

def parse_fasta(fasta_file):
    """
    Parses a FASTA file and extracts protein names and sequences.

    :param fasta_file: Path to the FASTA file
    :return: List of tuples containing (protein_name, protein_sequence)
    """
    proteins = []
    with open(fasta_file, 'r') as f:
        name, sequence = None, []
        for line in f:
            line = line.strip()
            if line.startswith('>'):
                if name:
                    proteins.append((name, ''.join(sequence)))
                name = line[1:]  # Remove '>' and use the rest as name
                sequence = []
            else:
                sequence.append(line)
        if name:
            proteins.append((name, ''.join(sequence)))
    return proteins

def create_json_files(proteins, output_dir):
    """
    Creates JSON files for each protein in the specified output directory.

    :param proteins: List of tuples containing (protein_name, protein_sequence)
    :param output_dir: Directory where JSON files will be saved
    """
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    for name, sequence in proteins:
        data = [
            {
                "name": name,
                "modelSeeds": [],
                "sequences": [
                    {
                        "proteinChain": {
                            "sequence": sequence,
                            "count": 1
                        }
                    }
                ]
            }
        ]
        json_file = os.path.join(output_dir, f"{name}.json")
        with open(json_file, 'w') as f:
            json.dump(data, f, indent=2)

        print(f"Created: {json_file}")

def main():
    parser = argparse.ArgumentParser(description="Generate JSON files from a FASTA file.")
    parser.add_argument("-input", required=True, help="Path to the input FASTA file")
    parser.add_argument("-output", required=True, help="Directory to save the JSON files")
    args = parser.parse_args()

    fasta_file = args.input
    output_dir = args.output

    proteins = parse_fasta(fasta_file)
    create_json_files(proteins, output_dir)

if __name__ == "__main__":
    main()
