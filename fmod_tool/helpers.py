import re
import logging

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


def extract(pdfdir, max_p):
    students = []
    for p in pdfdir.rglob("*.pdf"):
        p_name = p.stem
        names = re.findall("[A-Z][a-z]*", p_name)
        stud = Student(re.findall("\d+", p_name)[0], names[0], names[-1], names[1:-1], [0] * len(max_p))
        students.append(stud)
        logging.debug(stud)
    return students

