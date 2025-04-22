# AlphaFold3 Python Scripts

This repository contains a set of Python scripts that enhance AlphaFold3 outputs by adding useful visualizations and extracted data, such as:

- Average pLDDT scores as a CSV file
- PAE heatmap plots
- CIF-to-PDB conversions
- Grid visualizations of results
- Centralized collection of output files

---

## 📈 Create a CSV file with average pLDDT scores

```bash
python /home/$USER/af3_scripts/pLDDT.py ${OUTPUT_DIR}
```

This script parses all output structures in ==${OUTPUT_DIR}== and generates a CSV file with the average pLDDT score for each.

## 🔥 Create a PAE heatmap plot per structure

```bash
python /home/$USER/af3_scripts/pae.py ${OUTPUT_DIR}
```

Generates PAE (Predicted Aligned Error) heatmaps for each structure in the given output directory.

## 📦 Collect all CIF files into one folder

```bash
python /home/$USER/af3_scripts/collect_cifs.py -input ${OUTPUT_DIR}
```

Copies all .cif files from subdirectories into a single ==cifs/== folder within ==${OUTPUT_DIR}== for easy access.

## 🔄 Convert CIF files to PDB forma

```bash
python /home/$USER/af3_scripts/cif2pdb.py -input "${OUTPUT_DIR}/cifs" -output "${OUTPUT_DIR}/pdbs"
```

Converts all CIF structures into PDB format and saves them in a ==pdbs/== folder.

## 🧩 Generate a grid visualization

```bash
python /home/$USER/af3_scripts/grid.py --input_dir ${OUTPUT_DIR}
```

Creates a visual grid summary of predictions and structures within ==${OUTPUT_DIR}==.
