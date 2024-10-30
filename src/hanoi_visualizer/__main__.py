"""Command-line entry point for the solver and optional animation."""
import argparse

from . import solve


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("disks", type=int, nargs="?", default=3)
    parser.add_argument("--gui", action="store_true", help="open the animation")
    args = parser.parse_args()
    try:
        moves = solve(args.disks)
    except ValueError as error:
        parser.error(str(error))
    if args.gui:
        try:
            from .gui import show
        except ModuleNotFoundError as error:
            if error.name != "matplotlib":
                raise
            parser.error("Install the GUI with python -m pip install '.[gui]'.")
        show(args.disks)
    else:
        print(f"{len(moves)} moves")
        for source, target in moves:
            print(f"{'ABC'[source]} -> {'ABC'[target]}")


if __name__ == "__main__":
    main()
