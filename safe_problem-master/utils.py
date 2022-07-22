"""Utility functions."""


def read_input(file_path):
    """Read input text file.

    Args:
        file_path (str): path to input text file.

    Returns:
        (list): list of lines from input file.

    """
    with open(file_path, 'r') as f:
        contents = [line.strip() for line in f.readlines()]

    return contents


def write_to_file(results):
    """Write result string lines to text file.

    Args:
        results (list): list of strings.

    """
    with open("output.txt", "w") as out_file:
        for line in results:
            out_file.write(line + "\n")
