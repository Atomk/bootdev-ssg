import filegeneration
import os
import sys


def main():
    script_path = os.path.realpath(__file__)
    parent_dir = os.path.dirname(script_path)
    root_dir = os.path.realpath(os.path.join(parent_dir, ".."))
    public_dir_path = os.path.join(root_dir, "public")
    static_dir_path = os.path.join(root_dir, "static")
    content_dir_path = os.path.join(root_dir, "content")
    filegeneration.copy_directory_tree(static_dir_path, public_dir_path)
    filegeneration.generate_pages_recursive(
        content_dir_path,
        os.path.join(root_dir, "template.html"),
        public_dir_path,
    )
    print("Done")


main()
