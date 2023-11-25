import os
import argparse
import sys
import shutil

parser = argparse.ArgumentParser()


def file_backup(file, src, dest):
    parser.add_argument('--file', nargs='+', required=True, help='input file(s)')
    parser.add_argument('--src', nargs=1, required=True, help='directory of input file(s)')
    parser.add_argument('--dest', nargs=1, required=True, help='Intended destination for file')

    args = parser.parse_args(['--file', file, '--src', src, '--dest', dest])

    user_file = args.file
    src_directory = args.src[0]
    dest_directory = args.dest[0]

    for files in user_file:
        source_path = os.path.join(src_directory, files)
        try:
            backup_dest_1 = shutil.copy2(source_path, os.path.join((dest_directory + '_copy_of_' + files)))
        except FileNotFoundError:
            print(" %s Not Found in src directory " % files)
        try:
            backup_dest_2 = shutil.move(backup_dest_1, dest_directory)
        except shutil.Error as e:
            print(f"Error Moving file: {files} {e}")

    print("file move successful")


def dir_backup():
    parser.add_argument('--dir')
    parser.add_argument('--src')
    parser.add_argument('--dest')

    return 0


while True:
    userinput = input('would you like to backup a file or directory: ').lower()

    if userinput == "file":
        file = input('input filename(include extension): ')
        src = input('input directory file is in: ')
        dest = input('input destination you want file: ')
        file_backup(file, src, dest)
        break
    elif userinput == "directory":
        dir_backup()
        break
    elif userinput == "quit":
        sys.exit()
    else:
        print('invalid input: input "file", "directory", or "quit"')
