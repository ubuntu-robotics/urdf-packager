import argparse
import copy
import os
import shutil
import sys
import tarfile
import tempfile
import xml.etree.ElementTree as ET
from pathlib import Path

import resolve_robotics_uri_py


def parse_arguments():
    parser = argparse.ArgumentParser(description="Load a file from a given path.")
    parser.add_argument("file", help="The name of the file to load.")
    parser.add_argument(
        "-o", "--output-dir", default=".", help="The path where to save the archive."
    )
    parser.add_argument(
        '-p',
        "--package_dirs",
        default=None,
        nargs="+",
        help="The paths where the XML files are located. If not provided, uses the current working directory."
    )

    return parser.parse_args()

def check_file_exists(file_path):
    if not os.path.isfile(file_path):
        print(f"Error: '{file_path}' does not exist.")
        sys.exit(1)

def load_sdf_file(file_path):
    try:
        tree = ET.parse(file_path)
        return tree
    except ET.ParseError:
        print(f"Error parsing XML file '{file_path}': Invalid XML.")
        sys.exit(1)
    except Exception as e:
        print(f"Error loading XML file '{file_path}': {e}")
        sys.exit(1)

def find_and_resolve(tree, tag_name, package_dirs = None):
    update = copy.deepcopy(tree)
    files = []
    for elem in update.iter():
        if elem.tag == tag_name:
            uri = elem.text
            absolute_path = resolve_robotics_uri_py.resolve_robotics_uri(uri, package_dirs)
            elem.text = './' + os.path.basename(absolute_path)
            files.append(absolute_path)
    return update, files

def main():
    args = parse_arguments()

    check_file_exists(args.file)

    with tempfile.TemporaryDirectory() as tmp_dir_str:
        tmp_dir = Path(tmp_dir_str)

        file_copy = tmp_dir / os.path.basename(args.file)

        content = load_sdf_file(args.file)
        content, files = find_and_resolve(content, 'uri', args.package_dirs)

        content.write(file_copy, encoding="utf-8")

        # Copy files to the temporary directory
        for f in files:
            shutil.copy2(f, tmp_dir / os.path.basename(f))

        # Create tar.gz archive from the temporary directory
        archive_path = Path(args.output_dir) / "model.tar.gz"

        with tarfile.open(archive_path, "w:gz") as tarball:
            tarball.add(tmp_dir.resolve(), arcname='model')


if __name__ == "__main__":
    main()
