import os
import zipfile
import json
import csv

def rename_to_zip(file_path):
    new_path = os.path.splitext(file_path)[0] + '.zip'
    os.rename(file_path, new_path)
    return {"message": f"Renamed {file_path} to {new_path}", "new_path": new_path}

def unzip_file(file_path):
    with zipfile.ZipFile(file_path, 'r') as zip_ref:
        zip_ref.extractall()
    return {"message": f"Successfully extracted contents from {file_path}"}

def check_metadata():
    metadata_path = 'metadata'
    return os.path.exists(metadata_path)

def read_project_settings():
    with open('./Metadata/project_settings.config', 'r') as file:
        json_content = json.load(file)
    config = {
        "curr_bed_type": json_content.get("curr_bed_type"),
        "filament_settings_id": json_content.get("filament_settings_id")[0],
        "print_settings_id": json_content.get("print_settings_id"),
        "printer_settings_id": json_content.get("printer_settings_id"),
    }
    return config

def write_results_to_json(results):
    with open('results.json', 'w') as file:
        json.dump(results, file, indent=4)

if __name__ == "__main__":
    results = []
    folder_name = 'fileinput'
    rejected = False

    if os.path.exists(folder_name) and os.path.isdir(folder_name):
        files_in_folder = os.listdir(folder_name)
        results.append({"Files in folder": files_in_folder})
        
        for file_name in files_in_folder:
            file_to_extract = os.path.join(folder_name, file_name)
            if file_to_extract.lower().endswith('.3mf'):
                result = rename_to_zip(file_to_extract)
                results.append(result)
                unzip_result = unzip_file(result["new_path"])
                results.append(unzip_result)
                break
        else:
            results.append({"error": "This is not a .3mf file."})
            write_results_to_json(results)
            exit()

        if check_metadata():
            results.append({"message": "Metadata file exists."})

        settings = read_project_settings()
        inputPath = "validc.csv"
        with open(inputPath, newline='') as csvfile:
            valid = list(csv.reader(csvfile))

        for i, setting in enumerate(settings.values()):
            valid_values = valid[i+1]
            if setting not in valid_values:
                results.append({"WARNING": f"Invalid value found: {setting} is incorrect.",
                                "Valid settings": valid_values})
                rejected = True
            else:
                results.append({"message": f"{setting} is correct.", "Valid settings": valid_values})

        if not rejected:
            results.append({"message": "Your file is OK to be printed."})
        else:
            results.append({"error": "Please correct the indicated errors in your file."})
    else:
        results.append({"error": "Error: Metadata not found. Your file may not be sliced or may be otherwise invalid."})

    write_results_to_json(results)
