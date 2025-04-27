import filegeneration
import os
import sys


def main():
    script_path = os.path.realpath(__file__)
    parent_dir = os.path.dirname(script_path)
    public_dir_path = os.path.join(parent_dir, "..", "public")
    static_dir_path = os.path.join(parent_dir, "..", "static")
    filegeneration.copy_directory_tree(static_dir_path, public_dir_path)
    print("Done")


main()
