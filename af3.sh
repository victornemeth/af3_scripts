#!/bin/bash

cd /home/$USER/af3_runs/YOURDIR

# Define directories
INPUT_DIR="./input"
OUTPUT_DIR="./output"


MODEL_PARAMETERS_DIR="/mnt/NVME/af3.bin"  # Replace with the actual path to model parameters
DB_DIR="/mnt/NVME/AF3_DB_DIR"  # Replace with the actual path to the database directory

# Create the output directory if it doesn't exist
if [ ! -d "$OUTPUT_DIR" ]; then
    echo "Creating output directory: $OUTPUT_DIR"
    mkdir -p "$OUTPUT_DIR"
fi

# Run the Docker command
docker run -it \
    --volume "$INPUT_DIR:/root/af_input" \
    --volume "$OUTPUT_DIR:/root/af_output" \
    --volume "$MODEL_PARAMETERS_DIR:/root/models" \
    --volume "$DB_DIR:/root/public_databases" \
    --gpus device=3 \
    alphafold3 \
    python run_alphafold.py \
    --input_dir=/root/af_input \
    --model_dir=/root/models \
    --output_dir=/root/af_output

# Create a csv file with average pLDDT scores
python /home/$USER/af3_scripts/pLDDT.py ${OUTPUT_DIR}

# Create a PAE heatmap plot per structure in subfolder
python /home/$USER/af3_scripts/pae.py ${OUTPUT_DIR}

# Collect (copy) all cifs to one folder
python /home/$USER/af3_scripts/collect_cifs.py -input ${OUTPUT_DIR}

# Convert (copy) all cifs to pdbs
python /home/$USER/af3_scripts/cif2pdb.py -input "${OUTPUT_DIR}/cifs" -output "${OUTPUT_DIR}/pdbs"

# Create grid view
python /home/$USER/af3_scripts/grid.py --input_dir ${OUTPUT_DIR}

