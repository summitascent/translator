import argparse
from cli import in_terminal, main_menu, fallback_main_menu

def parse_args():
    parser = argparse.ArgumentParser(
        description="A universal dialogue translator which aims to make games "
                    "more accessible by breaking the language barrier."
    )
    parser.add_argument(
        "--verbose", "-v",
        action="store_true",
        help="enable *experimental* verbose functionality"
    )

    return parser.parse_args()


def main():
    args = parse_args()

    if in_terminal():
        main_menu(verbose=args.verbose)
    else:
        fallback_main_menu(verbose=True)


if __name__ == "__main__":
    main()
