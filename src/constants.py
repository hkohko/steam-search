from pathlib import PurePath

PROJ_DIR = PurePath(__file__).parents[1]
SRC = PROJ_DIR.joinpath("src")
FILES = SRC.joinpath("files")
