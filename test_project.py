import project, pytest, classes, data

def test_Weights():
    # Weights is a class in the student module
    with pytest.raises(ValueError):
        classes.Weights(0.5, 0.3, 0.1)
        classes.Weights(-0.1, 0.7, 0.4)

def test_subject():
    # subject is a class in the student module
    with pytest.raises(ValueError):
        classes.Subject("subject", "unit", -1, classes.Weights(0.5, 0.4, 0.1))
        classes.Subject("subject", "unit", 0, classes.Weights(0.5, 0.4, 0.1))


def test_student():
    # student is a class in the student module
    global student
    s = classes.Student("levi", "clark")
    assert(s.get_subject_score("english")) == 14.6
    assert(s.score(mode="invalid")) == 0
    with pytest.raises(ValueError):
        s.get_subject_score("invalid_subject")
    s = classes.Student("chloe", "foster")
    assert(project.rank(s)) == (1, [])
    s.gradesbook = {}
    assert(s.report()) == f"\n\n{classes.Color.blue}scores report {{    \n{classes.Color.blue}}}{classes.Color.reset}\n"


def test_data():
    assert(data.get_score("levi  ", "  clark", "english")) == [18, 9.5, 18]
    with pytest.raises(ValueError):
        data.get_average("invalid", classes.Weights(0.2, 0.2, 0.6))


def test_display():
    list = [
        {"name": "john harvard", "score": 20},
        {"name": "bruno mars", "score": 18},
        {"name": "marques brownee", "score": 19},
        {"name": "david milan", "score": 16},
              ]
    higher = project.display(list, colored=False)
    assert(next(higher)) == "01 : ---john harvard : 20.00"
    assert(next(higher)) == "02 : marques brownee : 19.00"
    assert(next(higher)) == "03 : -----bruno mars : 18.00"
    assert(next(higher)) == "04 : ----david milan : 16.00"


def test_rank():
    assert(project.rank(classes.Student("chloe", "foster"))) == (1, [])
    assert(project.rank(classes.Student("ethan", "sullivan"))) == (2, [{"name": "Chloe Foster", "score": 13.71}])
