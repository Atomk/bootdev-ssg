import os
import shutil
from nodeconversion import (
    markdown_to_html_tree,
)


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


def generate_page(from_path: str, template_path: str, dest_path: str, url_base: str):
    for p in (from_path, template_path):
        if not os.path.exists(p):
            raise ValueError(f"Path does not exist: {p}")
        if not os.path.isfile(p):
            raise ValueError(f"Path must be a file: {p}")
    if not from_path.endswith(".md"):
        raise ValueError(f"Source must be a Markdown (.md) file: {from_path}")
    if not template_path.endswith(".html"):
        raise ValueError(f"Template must be an HTML file: {template_path}")
    if not dest_path.endswith(".html"):
        raise ValueError(f"Destination must use a .html extension: {dest_path}")

    print(f"Generating page\n  from: {from_path}\n  to: {dest_path}\n  using: {template_path}")

    with open(from_path, encoding="utf-8") as f:
        markdown = f.read()
    with open(template_path, encoding="utf-8") as f:
        template = f.read()

    markdown_html = markdown_to_html_tree(markdown).to_html()
    title = extract_title(markdown)
    if not title:
        raise Exception(f"Page must have a title: {from_path}")

    PLACEHOLDER_TITLE = "{{ Title }}"
    PLACEHOLDER_CONTENT = "{{ Content }}"
    assert(PLACEHOLDER_TITLE in template)
    assert(PLACEHOLDER_CONTENT in template)
    replaced = template.replace(PLACEHOLDER_TITLE, title).replace(PLACEHOLDER_CONTENT, markdown_html)
    if url_base != "/":
        # TODO this will also replace the content of code blocks but should not
        replaced = replaced.replace(' href="/', f' href="{url_base}').replace(' src="/', f' src="{url_base}')

    # Assumes any necessary directories already exist
    with open(dest_path, "w", encoding="utf-8") as f:
        f.write(replaced)


def generate_pages_recursive(dir_path_content: str, template_path: str, dest_dir_path: str, url_base: str):
    """
    Converts all Markdown files in a directory (and in all of its subdirectories)
    into HTML pages. The hierarchy of directories is replicated at the new location.

    All internal links in the Markdown files are expected to start with the "/" character.

    Params:
        dir_path_content: Directory containing all source Markdown files
        template_path: HTML template file used for conversion
        dest_dir_path: Directory that will contain the generated output.
            Must be an existing path.
        url_base: used to add a prefix to all links.
    """

    for p in (dir_path_content, template_path, dest_dir_path):
        if not os.path.exists(p):
            raise ValueError(f"Path does not exist: {p}")
    for p in (dir_path_content, dest_dir_path):
        if not os.path.isdir(p):
            raise ValueError(f"Path must be a directory: {p}")
    if not template_path.endswith(".html"):
        raise ValueError(f"Template must be an HTML file: {template_path}")

    print(f"Output directory: {dest_dir_path}")
    print(f"URL base: {url_base}")

    def inner(source_dir: str, template: str, dest_dir: str):
        for filename in os.listdir(source_dir):
            new_source = os.path.join(source_dir, filename)
            new_dest = os.path.join(dest_dir, filename)
            if os.path.isdir(new_source):
                os.mkdir(new_dest)
                inner(new_source, template, new_dest)
            elif os.path.isfile(new_source):
                if not filename.endswith(".md"):
                    raise Exception(f"Found non-Markdown source file: {new_source}")
                new_dest_converted = new_dest.removesuffix(".md") + ".html"
                generate_page(new_source, template, new_dest_converted, url_base)
            else:
                raise Exception(f"Unrecognized file type at path: {new_source}")

    # TODO read the template file just once
    # with open(template_path, encoding="utf-8") as f:
    #     template = f.read()
    inner(dir_path_content, template_path, dest_dir_path)
