import os
import shutil
import argparse

def collect_cif_files(root_dir):
    cifs_dir = os.path.join(root_dir, "cifs")
    os.makedirs(cifs_dir, exist_ok=True)

    for current_dir, dirs, files in os.walk(root_dir):
        # Limit to depth 2 (root + 1 level)
        rel_depth = os.path.relpath(current_dir, root_dir).count(os.sep)
        if rel_depth > 0:
            continue

        for file in files:
            if file.endswith(".cif"):
                src_path = os.path.join(current_dir, file)
                dst_path = os.path.join(cifs_dir, file)

                # Avoid copying a file that's already in the target dir
                if os.path.abspath(src_path) != os.path.abspath(dst_path):
                    try:
                        shutil.copy2(src_path, dst_path)
                        print(f"✅ Copied: {src_path} → {dst_path}")
                    except Exception as e:
                        print(f"❌ Failed to copy {src_path}: {e}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Collect .cif files by copying them to a 'cifs' folder")
    parser.add_argument("-input", required=True, help="Path to the folder to search for .cif files")

    args = parser.parse_args()
    collect_cif_files(args.input)
