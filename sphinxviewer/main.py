import os
import sys

from argparse import ArgumentParser

from sphinxviewer.sphinx import build_html
from sphinxviewer.server import serve_server


def main():
    parser = ArgumentParser(description="Live editing sphinx doc server")
    # parser.add_argument("-p", "--port", default=8888, help="Port to run server on")
    # parser.add_argument("-d", "--build-dir", default="_build", help="Build directory")
    _ = parser.parse_args()
    print("Building initial docs")
    # TODO Parameterize source and build directories. Currently follows
    # the defaults for sphinx.
    success = build_html(os.getcwd(), "_build")
    if not success:
        sys.exit(1)
    serve_server(8888)
