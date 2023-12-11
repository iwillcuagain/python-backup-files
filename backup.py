import os
import argparse
import sys
import shutil
from datetime import date
import pdb

# Initialize the argument parser
common_parser = argparse.ArgumentParser(add_help=False)
common_parser.add_argument('--src', nargs=1, required=True, help='Source directory')
common_parser.add_argument('--dest', nargs=1, required=True, help='Destination directory')

# Parser for file_backup
file_backup_parser = argparse.ArgumentParser(parents=[common_parser])
file_backup_parser.add_argument('--file', nargs='+', required=True, help='Input file(s)')

# Parser for dir_backup
dir_backup_parser = argparse.ArgumentParser(parents=[common_parser])
dir_backup_parser.add_argument('--dir', nargs=1, required=True, help='Directory folder(s)')

# Get the current date in a specific format
today = date.today()
date_format = today.strftime("%d_%b_%Y_")


def save_value(new_name_path, dir_file):
    with open(dir_file, 'w') as f:
        f.write(new_name_path)


def load_value(dir_file):
    with open(dir_file, 'r') as f:
        read = f.read()
    return read.strip()


# makes the directory given by user into an usable directory
dir_file = 'values.txt'
values = load_value(dir_file)


def create_directory(directory):
    print(f"Loading in Previously set directory: {directory}")
    try:
        os.mkdir(directory)
        print(f"Directory loading successfully: {directory}")
    except FileExistsError:
        print("Directory loaded!")
    except Exception as e:
        print("No set Directory found.")


# Function for backing up individual files
def file_backup(file, src, dest):
    # Parse the command line arguments
    args = file_backup_parser.parse_args(['--file', file, '--src', src, '--dest', dest])

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
def dir_backup(folder_name, src, dest):
    # Parse the command line arguments
    args = dir_backup_parser.parse_args(['--dir', folder_name, '--src', src, '--dest', dest])
    user_folder = args.dir[0]
    src_directory = args.src[0]
    dest_directory = args.dest[0]

    print(f"Source directory: {os.path.join(src_directory, user_folder)}")
    print(f"Destination directory: {dest_directory}")

    # pdb.set_trace() *debugging via command-line*
    # Try to copy the entire directory to the destination
    try:
        shutil.copytree(os.path.join(src_directory, user_folder), os.path.join(dest_directory, user_folder))
    except FileNotFoundError:
        print(" Cannot find the path specified, re-check source destination")
    except FileExistsError:
        pass
    else:
        print("File move successful")
    return 0

    # Main loop for user interaction


def main():
    while True:
        userinput = input('would you like to backup a: \n (1) file \n (2) directory \n (3) setup fixed backup directory'
                          ' path '
                          'location \n (4) quit\n ')

        if userinput == "file" or userinput == '1':
            file = input('input filename(include extension): ')
            src = input('input directory file is in: ')
            # checks if  set dir path exists already
            if len(values) != 0:
                yes_path = input("Would you like to use previously set directory path? (y/n) ").lower()
                # calls file_backup with previously set path instead
                if yes_path == 'y':
                    file_backup(file, src, values)
                if yes_path == 'n':
                    dest = input('input destination you want file: ')
                    file_backup(file, src, dest)
            if len(values) == 0:
                dest = input('input destination you want file: ')
                file_backup(file, src, dest)
                break
        elif userinput == "directory" or userinput == '2':
            folder_name = input("input folder name: ")
            src = input('input directory location of folder: ')
            if len(values) != 0:
                yes_path = input("Would you like to use previously set directory path for backup? (y/n) ").lower()
                # calls file_backup with previously set path instead
                if yes_path == 'y':
                    dir_backup(folder_name, src, values)
                if yes_path == 'n':
                    dest = input('input destination you want folder: ')
                    dir_backup(folder_name, src, dest)
            if len(values) == 0:
                dest = input('input destination you want file(include the new file name you want it to be in e.g. '
                             'Desktop\\newfile): ')
                dir_backup(folder_name, src, dest)
                break
            break
        elif userinput == '3':
            try:
                new_path = input('input new directory path for future backups(not including actual '
                                 'folder) : ')
                name_path = input('What is the name you want to give the new backup folder: ')
                new_name_path = os.path.join(new_path, name_path)
                os.makedirs(new_name_path)
            except FileExistsError:
                save_value(new_name_path, dir_file)
                values = load_value(dir_file)
                print(f"Current Directory set!")

        elif userinput == "4":
            sys.exit()
        else:
            print('invalid input: input "file", "directory", or "quit"')


if __name__ == "__main__":
    create_directory(values)
    main()
