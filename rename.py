import os
import pandas as pd
from datetime import datetime
import shutil
from pprint import pprint




def reformat_scenar(scenar: str):
    if scenar.lower() == "saas":
        return "saas"
    elif scenar.lower() == "pbn":
        return "pbn"
    elif scenar.lower() == "10 backlinks":
        return "bk10"
    elif scenar.lower() == "20 backlinks":
        return "bk20"
    elif scenar.lower() == "30 backlinks":
        return "bk30"
    else:
        return ""

# Function to extract creation date from video file
def get_creation_date(file_path):
    return datetime.fromtimestamp(os.path.getctime(file_path))


# Function to rename and move video files
def rename_and_move_files(folder_path, file_names, domain_creation_dict):
    index = 0
    for file_name in file_names:
        file_path = os.path.join(folder_path, file_name)

        # Check if the file is a video file (you may need to modify the list of video extensions)
        if os.path.isfile(file_path) and file_path.lower().endswith(('.mp4', '.avi', '.mkv', '.mov')):
            # Extract domain from the file name
            domain = domain_creation_dict[index][0]
            scenar = reformat_scenar(domain_creation_dict[index][-1])
            index += 1
            # Construct the new file name
            new_file_name = f"{domain}_{scenar}.mp4"
            # Rename and move the file
            new_file_path = os.path.join(folder_path, new_file_name)
            shutil.move(file_path, new_file_path)
            print(f"File {file_name} renamed and moved to {new_file_path}")


def extract_creation_datetime(file_name):
    try:
        # Extract the date and time parts from the file name
        date_part, time_part = file_name.split(' ')[-2:]
        time_part = time_part.split(".")[0]
        # Combine date and time and convert to a datetime object
        creation_datetime = datetime.strptime(f"{date_part} {time_part}", '%Y-%m-%d %H-%M-%S')
        # print(creation_datetime, file_name)
        return creation_datetime
    except ValueError:
        print(file_name)
        # Handle the case where the date or time parts are not present or in an invalid format
        return None


def main():
    # Path to the folder containing the video files and the CSV file
    folder_path = 'C:/Users/User/Videos/Captures'
    csv_file_path = 'data/inputs/scenar - BK30.csv'

    # Get a list of files in the folder
    files = os.listdir(folder_path)
    sd = files.index('desktop.ini')
    files.pop(sd)
    # Sort the files based on creation date and time
    sorted_files = sorted(files, key=lambda x: extract_creation_datetime(x))

    # Read CSV file using pandas
    df = pd.read_csv(csv_file_path)

    # Create a dictionary mapping domain to creation date
    domain_creation_dict = [[row['domain'], row['Scenar'].lower()] for index, row in df.iterrows() if
                            row['Result'] in ['True', True]]

    rename_and_move_files(folder_path, sorted_files, domain_creation_dict)

main()