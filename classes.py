
from data import get_score, get_average, MAX_TITLE_LEN

class Color:
    def color_code(r, g, b):
        return f"\033[38;2;{r};{g};{b}m"


    blue = color_code(135, 115, 255)
    red = color_code(225, 59, 75)
    yellow = color_code(221, 175, 96)
    reset = f"\033[0m"


class Weights:
    def __init__(self, final, midterm, lab):
        tests = [final, midterm, lab]
        if all(v > 0 for v in tests) and round(sum(tests)) == 1:
            self.final = final
            self.midterm = midterm
            self.lab = lab
        else:
            raise ValueError(f"invalid weights : {tests}, within subject")


class Subject:
    """
    subject class
    """
    def __init__(self, name, unit, weight, weights):
        if weight <= 0:
            raise ValueError(f"negative subject weight: {weight}")
        self.name = name
        self.unit = unit
        self.weight = weight
        self.weights = weights

    def get_weights(self):
        return self.weights.final, self.weights.midterm, self.weights.lab


    def __str__(self):
        return f"{self.name}{{\n    unit: {self.unit}\n    weight: {self.weight}}}"


"""
pre-engineering students curriculum
"""

w1 = Weights(0.7, 0.2, 0.1)
w2 = Weights(0.6, 0.25, 0.15)
w3 = Weights(0.4, 0.4, 0.2)

analyse = Subject("calculus 3", "math", 1.5, w1)
algebre = Subject("algebra 3", "math", 1.5, w1)
se = Subject("os", "networds & systems", 1.5, w2)
tla = Subject("regex", "networds & systems", 1.5, w1)
reseau = Subject("networks fondamentals", "networds & systems", 1.5, w2)
transmission = Subject("data transmission", "networds & systems", 1, w1)
java = Subject("java", "programmin", 2, w2)
cpp = Subject("c++", "programming", 1, w2)
anglais = Subject("english", "languages", 1, w3)
francais = Subject("french", "languages", 1, w3)

curriculum = [anglais, analyse, algebre, se, tla, reseau, transmission, java, cpp, francais]


class Student:
    """
    pre-engineering student class
    """
    def __init__(self, first, last):
        self.first = first.capitalize().strip()
        self.last = last.capitalize().strip()
        self.gradesbook = [{"sid": subject.name, "score": get_score(self.first, self.last, subject.name)} for subject in curriculum]
        self._full_potential_score = self.score(mode="full_potential")
        self._proportional_score = self.score(mode="proportional")


    def get_subject_score(self, sid):
        for i in range(len(self.gradesbook)):
            if self.gradesbook[i]["sid"] == sid:
                # found the subject
                grades = self.gradesbook[i]["score"]
                weights = curriculum[i].get_weights()
                r = sum([grades[j] * weights[j] for j in range(3)]) / sum([weights[j] for j in range(3) if grades[j]])
                return r
        raise ValueError("f{sid} isn't available in your gradesbook")


    def score(self, mode=None):
        match mode.lower():
            case "proportional":
                total_score = 0
                for i in range(len(self.gradesbook)):
                    grade = sum(self.gradesbook[i]["score"][j] * curriculum[i].get_weights()[j] for j in range(3) if self.gradesbook[i]["score"][j])
                    if s := sum(curriculum[i].get_weights()[j] for j in range(3) if self.gradesbook[i]["score"][j]):
                        grade /= s
                    total_score += round(grade, 2) * curriculum[i].weight if grade else 0

                sum_subjects_weights_if_score = sum([curriculum[i].weight for i in range(len(curriculum)) if self.gradesbook[i]["score"] != [0, 0, 0]])
                return 0 if not(sum_subjects_weights_if_score) else total_score / sum_subjects_weights_if_score
            case "full_potential":
                total_score = 0
                for i in range(len(self.gradesbook)):
                    grade = sum(self.gradesbook[i]["score"][j] * curriculum[i].get_weights()[j] for j in range(3))
                    total_score += grade * curriculum[i].weight
                sum_subjects_weights = sum([s.weight for s in curriculum ])
                return total_score / sum_subjects_weights
            case _:
                return 0


    @property
    def first(self):
        return self._first
    @first.setter
    def first(self, first):
        self._first = first

    @property
    def last(self):
        return self._last
    @last.setter
    def last(self, last):
        self._last = last

    def __str__(self):
        return f"   {Color.red}----- proportional score: {Color.reset}{self._proportional_score:.2f}\n   {Color.red}-- full potentioal score: {Color.reset}{self._full_potential_score:.2f}"

    def report(self):
        submitted = [{"sid" : self.gradesbook[i]["sid"], "weights" : curriculum[i].get_weights()} for i in range(len(self.gradesbook)) if self.gradesbook[i]["score"] != [0, 0, 0]]
        output = f"\n\n{Color.blue}scores report {{    "
        for subject in submitted:
            output += f"\n    {Color.blue}-{subject['sid'].rjust(MAX_TITLE_LEN, '-')}: {Color.red if (self.get_subject_score(subject['sid']) >= get_average(subject['sid'], subject['weights'])) else Color.yellow}{self.get_subject_score(subject['sid']):.2F}"
        output += f"\n{Color.blue}}}{Color.reset}\n"
        return output

