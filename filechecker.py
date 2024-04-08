import os
import zipfile
import json
import csv

def rename_to_zip(file_path):
    new_path = os.path.splitext(file_path)[0] + '.zip'
    os.rename(file_path, new_path)
    print(f"Renamed {file_path} to {new_path}")
    return new_path

def unzip_file(file_path):
    with zipfile.ZipFile(file_path, 'r') as zip_ref:
        zip_ref.extractall()
    print(f"Successfully extracted contents from {file_path}")

def check_metadata():
    metadata_path = 'metadata'
    return os.path.exists(metadata_path)

def read_project_settings():
    # Read the JSON content from the file
    with open('./Metadata/project_settings.config', 'r') as file:
        json_content = json.load(file)

    # Access values directly from the JSON object
    bedtype = json_content.get("curr_bed_type")
    filament = json_content.get("filament_settings_id")
    profile = json_content.get("print_settings_id")
    printer = json_content.get("printer_settings_id")

    config = [bedtype, filament[0], profile, printer]
    return config
if __name__ == "__main__":
    folder_name = 'fileinput'

    # Check if the folder exists
    if os.path.exists(folder_name) and os.path.isdir(folder_name):
        # List all files in the specified folder
        files_in_folder = os.listdir(folder_name)
        print(f"Files in {folder_name} folder: {files_in_folder}")
        file_to_extract = os.path.join(folder_name, files_in_folder[0])
        print(f"File to extract: {file_to_extract}")
        if file_to_extract.lower().endswith('.3mf'):
            zip_file = rename_to_zip(file_to_extract)
        else: 
            file_to_extract = os.path.join(folder_name, files_in_folder[1])
            if file_to_extract.lower().endswith('.3mf'):
                zip_file = rename_to_zip(file_to_extract)
            else:
                 print("This is not a .3mf file.")
                 exit()
        unzip_file(zip_file)
        print(f"{file_to_extract} has been successfully renamed to {zip_file} and extracted.")

        # Check for the existence of the 'metadata' file
        if check_metadata():
                    print("Metadata file exists.")
                    
        # Read and print the content of 'project_settings.config'
        validbed = ["Cool Plate"]
        validfil = ['Bambu PLA Basic @BBL X1C', 'Generic PLA @BBL X1C']
        validprof = ["0.20mm Standard @BBL X1C", "0.20mm Strength @BBL X1C", "0.16mm Optimal @BBL X1C", "0.24mm Draft @BBL X1C", "0.12mm Fine @BBL X1C"]
        validprinter = "Bambu Lab X1 Carbon 0.4 nozzle"
        # Import the acceptable settings
        inputPath = "validc.csv"

        players = []
        with open(inputPath, newline='') as csvfile:
            valid = list(csv.reader(csvfile))

        settings = read_project_settings()
        rejected = False

        for i in range(len(settings)):
            if settings[i] not in valid[i+1]:
                print("WARNING!! Invalid values found.") 
                print(settings[i] + " is incorrect.")
                print("Valid settings include: ")
                for thing in valid[i+1]:
                     print(thing)
                rejected=True  
            if settings[i]  in valid[i+1]:
                print("This is OK..") 
                print(settings[i] + " is correct.")
                print("Valid settings include: ")
                for thing in valid[i+1]:
                     print(thing)
            

#        if settings[0]!= validbed [1][0]:
#            print("fucked up bed settings")
#            rejected = True
#        if ((settings[1] != validfil[0]) and (settings[0] != validfil[1])):
#            print("fucked up filament")
#            rejected = True
#        if ((settings[2]!=validprof[0])and(settings[2]!=validfil[1])and(settings[2]!=validprof[3])and(settings[2]!=validfil[4])):
#            print("fucked up profile")
#            rejected = True
#        if settings[3]!= validprinter:
#            print("big fuck up")
#            rejected = True  """

    if rejected == False:
        print("Your file is OK to be printed.")
    else:
            print("Please correct the indicated errors in your file. ")
else:
    print("Error: Metadata not found. Your file may not be sliced or may be otherwise invalid.")

