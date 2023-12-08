import os
import argparse
import sys
import shutil
from datetime import date
import pdb

# Initialize the argument parser
parser = argparse.ArgumentParser()

# Get the current date in a specific format
today = date.today()
date_format = today.strftime("%d_%b_%Y_")


# Function for backing up individual files
def file_backup(file, src, dest):
    # Define command line arguments for file backup
    parser.add_argument('--file', nargs='+', required=True, help='input file(s)')
    parser.add_argument('--src', nargs=1, required=True, help='directory of input file(s)')
    parser.add_argument('--dest', nargs=1, required=True, help='Intended destination for file')

    # Parse the command line arguments
    args = parser.parse_args(['--file', file, '--src', src, '--dest', dest])

    # Extract user inputs from parsed arguments
    user_file = args.file[0]
    user_file = user_file.split(' ')
    src_directory = args.src[0]
    dest_directory = args.dest[0]

    # pdb.set_trace() *debugging via command-line*
    # Loop through each file and perform backup
    for files in user_file:
        source_path = os.path.join(src_directory, files)
        try:
            backup_dest_1 = shutil.copy2(source_path, os.path.join((dest_directory + "_" + date_format + files)))
        except FileNotFoundError:
            print(" %s Not Found in src directory " % files)
        try:
            backup_dest_2 = shutil.move(backup_dest_1, dest_directory)
        except shutil.Error as e:
            print(f"Error Moving file: {files} {e}")

    print("file move successful")


# Function for backing up entire directories
def dir_backup(directory, src, dest):
    # Define command line arguments for directory backup
    parser.add_argument('--dir', nargs=1, required=True, help='Directory folder(s)')
    parser.add_argument('--src', nargs=1, required=True, help='directory of input folders')
    parser.add_argument('--dest', nargs=1, required=True, help='Intended destination for folder')

    # Parse the command line arguments
    args = parser.parse_args(['--dir', directory, '--src', src, '--dest', dest])
    user_folder = args.dir[0]
    src_directory = args.src[0]
    dest_directory = args.dest[0]

    # pdb.set_trace() *debugging via command-line*
    # Try to copy the entire directory to the destination
    try:
        shutil.copytree(src_directory, os.path.join(dest_directory + '\\', user_folder))
    except FileNotFoundError:
        print(" Cannot find the path specified, re-check source destination")
    except FileExistsError:
        print(" The folder in dest_directory already exists, if not, re-check dest_directory location")
    else:
        print("File move successful")
    return 0


# Main loop for user interaction
while True:
    userinput = input('would you like to backup a file or directory: ').lower()

    if userinput == "file":
        file = input('input filename(include extension): ')
        src = input('input directory file is in: ')
        dest = input('input destination you want file: ')
        file_backup(file, src, dest)
        break
    elif userinput == "directory":
        directory = input("input directory name: ")
        src = input('input directory location: ')
        dest = input('input destination you want file: ')
        dir_backup(directory, src, dest)
        break
    elif userinput == "quit":
        sys.exit()
    else:
        print('invalid input: input "file", "directory", or "quit"')
