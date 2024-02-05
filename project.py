from data import grades, titles
from student import Student, Color as c
import sys, inflect
p = inflect.engine()


def main():
    print("submitted subjects:", p.join(titles))
    try:
        first, last = input(f"{c.red}Student{{\n{c.red}   -------------- full name: {c.reset}").strip().split()
    except ValueError:
        sys.exit("invalid name, input you first and last name")

    student = Student(first, last)
    # add rank manually along with the report
    print(student)
    r, sup = rank(student)
    print(f"   {c.red}---------------- ranking: {c.reset}{p.ordinal(r)}\n{c.red}}}{c.reset}")

    print(student.report())
    higher = display(sup)
    for student in higher:
        print(student)

def display(d, colored=True):
    try:
        m = max(len(s['name']) for s in d)
    except ValueError:
        print("you're the best ⭐\n")
        return None
    for index, s in enumerate(sorted(d, key=lambda s: s["score"], reverse=True)):
        yield (f"{index+1:02} : {s['name'].rjust(m, '-')} : {c.red if colored else ''}{s['score']:.2f}{c.reset if colored else ''}")

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


if __name__ == "__main__":
    main()
