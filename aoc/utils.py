import pathlib

CURRENT_PATH = pathlib.Path(__file__).parent.absolute().parent.absolute()


def read_lines(path, strip=False):
    with open(f"{CURRENT_PATH}/data/{path}", "r") as file_:
        line = file_.readline()

        while line:
            if strip:
                yield line.strip()
            else:
                yield line
            line = file_.readline()


def read_file(path):
    data = ""
    with open(f"{CURRENT_PATH}/data/{path}", "r") as file_:
        data = file_.read()
    return data
