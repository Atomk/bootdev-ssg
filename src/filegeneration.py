import os
import shutil


# similar to shutil.rmtree()
def delete_directory_tree(dir_path: str):
    if not os.path.exists(dir_path):
        raise ValueError(f"Path destination does not exist: {dir_path}")
    if not os.path.isdir(dir_path):
        raise ValueError(f"Path is not a directory: {dir_path}")

    def inner(dirpath):
        for filename in os.listdir(dirpath):
            filepath = os.path.join(dirpath, filename)
            if os.path.isdir(filepath):
                inner(filepath)
                os.rmdir(filepath)
            elif os.path.isfile(filepath):
                os.remove(filepath)
            else:
                raise Exception(f"Unrecognized file type at path: {filepath}")

    inner(dir_path)
    os.rmdir(dir_path)


def copy_directory_tree(source_path: str, dest_path: str):
    if os.path.exists(dest_path):
        if not os.path.isdir(dest_path):
            raise ValueError(f"Destination path is not a directory: {dest_path}")
        delete_directory_tree(dest_path)

    os.mkdir(dest_path)

    if not os.path.isdir(source_path):
        raise ValueError(f"Source path is not a directory: {source_path}")

    _copy_directory_tree_inner(source_path, dest_path)


# Extracted from main function to prevent accidentally accessing
# nonlocal variables (they have very similar names)
def _copy_directory_tree_inner(source_dir, dest_dir):
    for filename in os.listdir(source_dir):
        new_source = os.path.join(source_dir, filename)
        new_dest = os.path.join(dest_dir, filename)
        if os.path.isdir(new_source):
            os.mkdir(new_dest)
            _copy_directory_tree_inner(new_source, new_dest)
        elif os.path.isfile(new_source):
            shutil.copy(new_source, new_dest)
        else:
            raise Exception(f"Unrecognized file type at path: {new_source}")


def extract_title(markdown: str):
    for line in markdown.splitlines():
        stripped = line.lstrip()
        if stripped.startswith("# "):
            return stripped.lstrip("#").strip().replace("\n", " ")
    raise ValueError("Title not found")
