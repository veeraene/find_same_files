#
# Finds files with the same suffix and same contents. The file suffix is case insensitive.
# Usage: python find_same_files.py root_directory file_suffix
#
# or
# import find_same_files
# find_same_files.find_same_files(root_directory, file_suffix)
#

import sys
import glob
import os
import filecmp


def group_by_length(files_by_length, path_pattern):
    for file_name in glob.iglob(path_pattern, recursive=True):
        size = os.path.getsize(file_name)
        if size in files_by_length:
            files_by_length[size].append(file_name)
        else:
            files_by_length[size] = [file_name]


def find_same_files(root_directory, file_suffix):
    files_by_length = {}
    group_by_length(files_by_length, root_directory + '/**/*' + file_suffix.lower())
    group_by_length(files_by_length, root_directory + '/**/*' + file_suffix.upper())

    # List of lists of files with same length
    all_same_length_files = []
    for files_with_same_length in files_by_length.values():
        if len(files_with_same_length) > 1:
            all_same_length_files.append(files_with_same_length)

    #print('Files with same lengths:')
    #print(all_same_length_files)
    #print()

    # List of lists of files with same first 256 bytes
    all_files_with_same_first_bytes = []
    for files_with_same_length in all_same_length_files:
        files_by_first_bytes = {}
        for file_name in files_with_same_length:
            with open(file_name, 'rb') as file:
                first_bytes = file.read(256)

            if first_bytes in files_by_first_bytes:
                files_by_first_bytes[first_bytes].append(file_name)
            else:
                files_by_first_bytes[first_bytes] = [file_name]

        for files_with_same_first_bytes in files_by_first_bytes.values():
            if len(files_with_same_first_bytes) > 1:
                all_files_with_same_first_bytes.append(files_with_same_first_bytes)

    #print('Files with same first bytes:')
    #print(all_files_with_same_first_bytes)
    #print()

    # List of lists of files with same contents
    all_files_with_same_content = []
    for files_with_same_first_bytes in all_files_with_same_first_bytes:
        # [[file_a_1, file_a_2, file_a_3], [file_b_1, file_b_2]]
        same_content_files = []

        for file_name in files_with_same_first_bytes:
            found_match = False
            # Find a match in the lists of files with same contents
            for list_of_same_content_files in same_content_files:
                # Compare the file with the first item in the group of same content files
                if filecmp.cmp(file_name, list_of_same_content_files[0], shallow=False):
                    list_of_same_content_files.append(file_name)
                    found_match = True
                    break
            if not found_match:
               same_content_files.append([file_name])

        all_files_with_same_content.extend(same_content_files)

    all_files_with_same_content_more_than_one = []
    for files_with_same_content in all_files_with_same_content:
        if len(files_with_same_content) > 1:
            all_files_with_same_content_more_than_one.append(files_with_same_content)

    return all_files_with_same_content_more_than_one


def main():
    if len(sys.argv) != 3:
        raise ValueError(f'Usage: {sys.argv[0]} ROOT SUFFIX')

    files_with_same_content = find_same_files(sys.argv[1], sys.argv[2])

    print('Files with same contents:')
    print(files_with_same_content)


if __name__  == "__main__":
    main()