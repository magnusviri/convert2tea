import argparse
from pprint import pprint


def parse(args):
    parser = argparse.ArgumentParser(
        "convert2tea", description="Convert formula to tea using AI"
    )
    parser.add_argument(
        "language", type=str, nargs=1, help="Language: i.e. c, python, ruby, go"
    )
    parser.add_argument("project", type=str, nargs=1, help="Project name")
    parser.add_argument(
        "filepath", type=str, nargs=1, help="Path to Homebrew .rb formula to convert"
    )
    parser.add_argument(
        "-v", "--version", action="store_true", help="print version and exit"
    )
    parser.add_argument(
        "-n", "--dry-run", action="store_true", help="print prompt and exit"
    )
    options = parser.parse_args(args)
    return options
