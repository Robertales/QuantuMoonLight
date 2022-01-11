import os
from datetime import datetime
from pathlib import Path


def log():
    dataora = datetime.now()

    # dd/mm/YY H:M:S
    dt_string = dataora.strftime("%d/%m/%Y %H:%M:%S")
    print("\n", dt_string)
    print("\n")
    ROOT_DIR = Path(__file__).parents[2].__str__()

    file1 = open(ROOT_DIR + "\\log\\log.txt ", "a+")

    file1.write(dt_string + "\n")
    file1.close()


# datetime object containing current date and time
