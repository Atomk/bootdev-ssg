import filegeneration
import os
import sys


def parse_arguments() -> tuple[str, str]:
    if len(sys.argv) > 3:
        raise Exception(f"Passed too many arguments ({len(sys.argv) - 1})")

    if len(sys.argv) < 2:
        raise Exception("Missing the required argument")
    output_dir_name = sys.argv[1]
    if not output_dir_name.isalnum():
        raise Exception("Output directory name must be alphanumeric")

    url_base = "/"
    if len(sys.argv) == 3:
        url_base = sys.argv[2]
        if not url_base.endswith("/"):
            raise Exception("URL base must end with the '/' character")

    return output_dir_name, url_base


def main():
    try:
        output_dir_name, url_base = parse_arguments()
    except Exception as e:
        print(f"There was en arror while parsing arguments:\n  {e}")
        print("Usage:\n  main.py output-dir-name <base-url>\n")
        sys.exit(1)

    script_path = os.path.realpath(__file__)
    parent_dir = os.path.dirname(script_path)
    root_dir = os.path.realpath(os.path.join(parent_dir, ".."))
    output_dir_path = os.path.join(root_dir, output_dir_name)
    static_dir_path = os.path.join(root_dir, "static")
    content_dir_path = os.path.join(root_dir, "content")
    filegeneration.copy_directory_tree(static_dir_path, output_dir_path)
    filegeneration.generate_pages_recursive(
        content_dir_path,
        os.path.join(root_dir, "template.html"),
        output_dir_path,
        url_base,
    )
    print("Done")


main()
