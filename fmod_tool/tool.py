#!/usr/bin/python3

import click
import click_pathlib
import re
import logging
import pandas as pd
import numpy as np

# other deps
import tabulate
import xlrd
import openpyxl

logging.basicConfig(level=logging.DEBUG)

max_p = {
        "1": 3,
        "2": 4,
        "3": 4,
        "4": 4,
        "5": 3,
        "6": 3,
        "7": 3,
        "8": 2,
        "9": 2,
        "10": 4,
        "11": 4,
        "12": 3,
        "13": 3,
        "14": 4,
        "15": 4
        }


def get_done(df, done_dir):
        done_mnr = []
        for p in done_dir.rglob("*.pdf"):
             done_mnr.append(re.findall("\d+", p.stem)[0])
        return df[df.MN.isin(done_mnr)]

def get_not_done(df, not_done_dir):
        not_done_mnr = []
        for p in not_done_dir.rglob("*.pdf"):
            not_done_mnr.append(re.findall("\d+", p.stem)[0])
        return df[df.MN.isin(not_done_mnr)]

class Student:
    def __init__(self, mn, vn, nn, en, points):
        self.mn = mn
        self.vn = vn
        self.nn = nn
        self.en = en
        self.points = points
    
    def __str__(self):
        t = f"{self.mn},{self.vn},{self.nn},"
        for p in self.points:
            t += f"{p},"
        t += ";".join(self.en)
        return t

def extract(pdfdir):
    students = []
    for p in pdfdir.rglob("*.pdf"):
        p_name = p.stem
        names = re.findall("[A-Z][a-z]*", p_name)
        stud = Student(re.findall("\d+", p_name)[0], names[0], names[-1], names[1:-1], [0] * len(max_p))
        students.append(stud)
        logging.debug(stud)
    return students

@click.group()
def tools():
    pass

@tools.command(name="extract")
@click.argument("pdfdir", default="not_done", type=click_pathlib.Path(exists=True, file_okay=False))
@click.option("-o", "--output", default="names.txt", type=click_pathlib.Path(exists=False, dir_okay=False))
def extract_command(pdfdir, output):
    header = f"MN,VN,NN,"
    for a,_ in max_p.items():
        header += f"{a},"
    header += f"EN\n"
    students = extract(pdfdir)
    with output.open("w") as o:
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
@click.argument("NAMESTXT", default="names.txt", type=click_pathlib.Path(exists=True, dir_okay=False))
@click.argument("not_done_dir", default="not_done", type=click_pathlib.Path(exists=True, file_okay=False))
@click.argument("done_dir", default="done", type=click_pathlib.Path(exists=True, file_okay=False))
def correct(matnr, namestxt, not_done_dir, done_dir):
    df = read_names(namestxt)
    print(get_done(df, done_dir))
    studrow = df[df.MN == matnr].copy()
    print(studrow)
    points = []
    for a,v in max_p.items():
        print(f"MAX POINTS FOR {a:<2}:{v:>2}")
        p = None
        while(p == None):
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
    df.to_csv(namestxt, index=False)
    df = read_names(namestxt)
    pdf = next(not_done_dir.rglob(f"{matnr}*.pdf"))
    pdf.rename(done_dir / (pdf.stem + "_copy.pdf"))
    print(get_not_done(df, not_done_dir))

@tools.command(name="show")
@click.argument("NAMESTXT", default="names.txt", type=click_pathlib.Path(exists=True, dir_okay=False))
@click.argument("not_done_dir", default="not_done", type=click_pathlib.Path(exists=True, file_okay=False))
@click.argument("done_dir", default="done", type=click_pathlib.Path(exists=True, file_okay=False))
@click.option("-d", "--done", is_flag=True, default=False)
def show(namestxt, not_done_dir, done_dir, done):
    df = read_names(namestxt)
    if done:
        print("DONE:")
        print(get_done(df, done_dir))
        print()
    else:
        print("NOT DONE:")
        print(get_not_done(df, not_done_dir))
        print()

@tools.command(name="to_xlsx")
@click.argument("EXCELFILE", type=click_pathlib.Path(exists=True, dir_okay=False))
@click.argument("tutorname", envvar="TUTN", type=click.STRING, required=True)
@click.argument("NAMESTXT", default="names.txt", type=click_pathlib.Path(exists=True, dir_okay=False))
def to_xlsx(excelfile, namestxt, tutorname):
    xl = pd.read_excel(excelfile, dtype={"ID-Nummer": "string"})
    punkte_col = next(s for s in xl.columns if s.endswith("Punkte"))
    df = read_names(namestxt)
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
