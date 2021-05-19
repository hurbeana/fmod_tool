#!/usr/bin/python3

import click
import click_pathlib
import pandas as pd
from yaml import load, SafeLoader

from .default_settings import *
from .helpers import *

logging.basicConfig(level=logging.DEBUG)

if not settings_file.exists():
    settings_file.write_text(default_settings)
    print(
        "[INFO]: Default Settings file create in current directoy [settings.yml].\nPlease edit it and retry your last "
        "command.")
    exit(0)

if not done_path.exists():
    print("[ERROR]: Missing 'done' directory, please create it before proceeding")
    exit(-1)

if not not_done_path.exists():
    print("[ERROR]: Missing 'not_done' directory, please create it and put pdfs into it before proceeding")
    exit(-1)

if not names_txt_path.exists():
    print("[ERROR]: Please run the extract command first, names.txt missing")
    exit(-1)

settings = load(settings_file.read_text(), Loader=SafeLoader)
try:
    max_p = {k: int(v) for k, v in settings["Maximum Points"].items()}
except ValueError:
    print("Please provide numbers for the points")
    exit(-1)
after_finish = settings["After Finish"]


@click.group()
def tools():
    pass


@tools.command(name="extract")
def extract_command():
    """
    Looks into all pdfs that are in the not_done directory and outputs the to names.txt
    """
    header = f"MN,VN,NN,"
    for a, _ in max_p.items():
        header += f"{a},"
    header += f"EN\n"
    students = extract(not_done_path)
    with names_txt_path.open("w") as o:
        o.write(header)
        o.write("\n".join(str(s) for s in students))
        o.write("\n")


def read_names(csv, pr=False):
    df = pd.read_csv(csv, dtype={'MN': 'string'})
    if pr:
        print()
        print(df)
        print()
    return df


@tools.command(name="correct")
@click.argument("MATNR", type=click.STRING)
def correct(matnr):
    """
    Starts one correction of the given MATNR. PDF with the same MATNR needs to exist in the not_done folder.
    After the last enter, the chosen action from settings.yml will be taken (NOTHING | REMOVE | RENAME).
    """
    df = read_names(names_txt_path)
    print(get_done(df, done_path))
    studrow = df[df.MN == matnr].copy()
    print(studrow)
    points = []
    for a, v in max_p.items():
        print(f"MAX POINTS FOR {a:<2}:{v:>2}")
        p = None
        while p is None:
            try:
                inp = input(F"Enter Points: ")
                if inp == "":
                    p = v
                else:
                    p = int(inp)
                if p > v:
                    print(f"Points higher than max points [{v}] for this ex {a}")
                    p = None
            except ValueError:
                print("Invalid value")
                pass
        studrow[a] = p
        points.append(p)
        print(studrow)
    print()
    print("SUM: " + str(studrow.sum(axis=1).values[0]))
    print()
    input("Press key to move pdf to done...")
    df[df.MN.isin(studrow.MN)] = studrow
    df.to_csv(names_txt_path, index=False)
    df = read_names(names_txt_path)
    pdf = next(not_done_path.rglob(f"{matnr}*.pdf"))
    if after_finish == "REMOVE":
        pdf.unlink()
    elif after_finish == "RENAME":
        pdf.rename(done_path / (pdf.stem + "_copy.pdf"))
    print(get_not_done(df, not_done_path))


@tools.command(name="show")
@click.option("-d", "--done", is_flag=True, default=False)
def show(done):
    """
    Shows not done hand ins in a tabular format.
    If -d is given, shows the done hand ins
    """
    df = read_names(names_txt_path)
    if done:
        print("DONE:")
        print(get_done(df, done_path))
        print()
    else:
        print("NOT DONE:")
        print(get_not_done(df, not_done_path))
        print()


@tools.command(name="to_xlsx")
@click.argument("EXCELFILE", type=click_pathlib.Path(exists=True, dir_okay=False))
@click.argument("tutorname", envvar="TUTN", type=click.STRING, required=True)
def to_xlsx(excelfile, tutorname):
    """
    Exports results from names.txt to the given EXCELFILE with given TUTORNAME. You can also set the TUTN environment
    variable to pass this in. The original excel will not be edited, a new one with _done.xlsx will be created.
    """
    xl = pd.read_excel(excelfile, dtype={"ID-Nummer": "string"})
    punkte_col = next(s for s in xl.columns if s.endswith("Punkte"))
    df = read_names(names_txt_path)
    df.set_index("MN", inplace=True)
    df["sum"] = df.sum(axis=1).astype(int)
    print(df)
    xl["idx"] = xl["ID-Nummer"]
    xl.set_index("idx", inplace=True)
    xl.loc[df.index, punkte_col] = df["sum"]
    xl.loc[df.index, "TutorIn"] = tutorname
    xl.to_excel(excelfile.stem + "_done.xlsx", index=False)


if __name__ == "__main__":
    tools()
