import os

from typing import Optional, List
from subprocess import run


def build_html(source_dir: str, build_dir: str, files: Optional[List[str]] = None) -> bool:
    """build_html relies on the `sphinx-build` command.

    Args:
        source_dir (str): Directory that contains rst to be built
        build_dir (str): Directory to output build files to
        files (:obj:`list`, optional): List of file paths to build specifically.
            Useful if build time for complete docs is significantly longer.

    Returns:
        bool: True, docs built successfully.
    """
    args = ["sphinx-build", "-j", "auto", source_dir, f"{build_dir}/html/"]
    if files is not None:
        for path in files:
            args.append(path)
    proc = run(args, check=False)
    if proc.returncode != 0:
        print("No docs in the current directory, run from a doc directory")
        return False
    if not os.path.isdir(build_dir):
        print(f"Unable to find build directory: {build_dir}")
        return False
    html_dir = os.path.join(build_dir, "html")
    if not os.path.isdir(html_dir):
        print(f"Unable to find html directory: {html_dir}")
        return False
    return True
