import shutil as sh
import os

tokens = []

with open("DATABASES/base1.css", 'r') as css:
    lines = css.readlines()
    comment = False

    # parse
    for line in lines:
        stripped_line = line.strip()
        if stripped_line.startswith("/*"):
            comment = True
        if not comment:
            if stripped_line.startswith("color: #"):
                stripped_line = stripped_line.removeprefix("color: #")
                stripped_line = stripped_line.removesuffix(";")
                tokens.append(stripped_line)
        if stripped_line.endswith("*/"):
            comment = False

    print(tokens)