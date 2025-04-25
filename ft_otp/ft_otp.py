import argparse
import os


def parse_args():
    parser = argparse.ArgumentParser(description="File Transfer OTP Generator")
    parser.add_argument("-g", "--generate", help="Generate and store the key", type=str)
    parser.add_argument("-k", "--key", help="Generate OTP from stored key", action="store_true")

    args = parser.parse_args()
    return args

def main():
    args = parse_args()


if __name__ == "__main__":
    main()