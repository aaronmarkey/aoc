import pathlib


def read_lines(path, strip=False):
    current_path = pathlib.Path(__file__).parent.absolute()
    with open(f"{current_path}/data/{path}", "r") as file_:
        line = file_.readline()

        while line:
            if strip:
                yield line.strip()
            else:
                yield line
            line = file_.readline()


def read_file(path):
    current_path = pathlib.Path(__file__).parent.absolute()
    data = ""
    with open(f"{current_path}/data/{path}", "r") as file_:
        data = file_.read()
    return data
