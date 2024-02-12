from classes import Color, Student
import sys, inflect
p = inflect.engine()
from data import titles, grades

def main():
    print(f"{Color.red}submitted subjects:{Color.blue}", p.join(titles), f"{Color.reset}\n")
    try:
        first, last = input(f"{Color.red}Student{{\n{Color.red}   -------------- full name: {Color.reset}").strip().split()
    except ValueError:
        sys.exit("invalid name, input you first and last name")
    try:
        student = Student(first, last)
        # add rank manually along with the report
        print(student)
        r, sup = rank(student)
        print(f"   {Color.red}---------------- ranking: {Color.reset}{p.ordinal(r)}\n{Color.red}}}{Color.reset}")
        print(student.report())
        print(average_student())
        higher = display(sup)
        for student in higher:
            print(student)
    except ValueError as ve:
        sys.exit(str(ve))


def display(d, colored=True):
    try:
        m = max(len(s['name']) for s in d)
    except ValueError:
        print("you're the best ⭐\n")
        return None
    for index, s in enumerate(sorted(d, key=lambda s: s["score"], reverse=True)):
        yield (f"{index+1:02} : {s['name'].rjust(m, '-')} : {Color.red if colored else ''}{s['score']:.2f}{Color.reset if colored else ''}")

def rank(user):
    rank = 1
    score = user._proportional_score
    sup = []
    for row in grades:
        first, last = row[0], row[1]
        student = Student(first.strip().capitalize(), last.strip().capitalize())
        test_score = student._proportional_score
        if score < test_score:
            sup.append({"name": f"{student.first} {student.last}", "score":round(test_score, 2)})
            rank += 1
    return rank, sup

def average_student():
    total = [Student(name[0], name[1]).score(mode="proportional") for name in grades]
    n = len(total)
    total = sum(total)
    return(f"{Color.blue}{{\n    average student score: {Color.red}{total/n:.2f}\n{Color.blue}}}{Color.reset}\n")




if __name__ == "__main__":
    main()
