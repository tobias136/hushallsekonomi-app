# scripts/reset_test_data.py

import os
import glob


def reset_data_folder():
    data_dir = "data"

    if not os.path.exists(data_dir):
        print("Data-mappen finns inte. Inget att radera.")
        return

    # Radera kategorier.json om den finns
    kategorier_path = os.path.join(data_dir, "kategorier.json")
    if os.path.exists(kategorier_path):
        os.remove(kategorier_path)
        print(f"Raderade: {kategorier_path}")

    # Radera alla import_*.json-filer
    import_files = glob.glob(os.path.join(data_dir, "import_*.json"))
    for filepath in import_files:
        os.remove(filepath)
        print(f"Raderade: {filepath}")

    print("Återställning av testdata klar.")


if __name__ == "__main__":
    reset_data_folder()
