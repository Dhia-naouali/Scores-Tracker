# Scores Tracker
### Video Demo:  [youtube](https://www.youtube.com/watch?v=GCAWtp-DgIo)
### Description:

**Scores Tracker** is a python program that, given a Google Sheets spreadsheet that includes a class's scores, will prompt the user for their full name
to output their overall score, their ranking in the class, and their scores in each subject

## Users Manual

### Features

1. **Data**:
   - Accessing data from your Google Sheets spreadsheet through an API.
   - the spreadsheet includes the final, midterm, and lab/project scores for each subject for all students
     (not necessarily all scores are available at the moment of use).

2. **Input and Output**:
   - Input: Provide a student's first and last name.
   - Output:
     - Overall score for the student.
       - proportional to the currently submitted scores
       - assuming that the rest of the score to be submitted will be zero (the minimum score you'll get)
     - Rank of the student among all students.
     - Individual subject scores (color-coded to indicate above/below average).
     - List of higher-ranking students and their overall scores.


3. **Prerequisites**:
   - The Google Sheets spreadsheet API
   - The mentioned modules/libraries in the requirements file

### Setup

1. **Install the requirements**:
   - using pip install "module_name" (in your terminal window)

2. **Set your curriculum**
   - in the data section in the project.py file set the name, unit, weight, and weights for each subject in the curriculum list

### Usage

1. **Run the Program**:
   - run "python project.py"
   - Input your first and last name when prompted.


## Development process

**Scores Tracker** is my final project as part of the CS50P course
I came up with the idea as a response to a need
the college, that I'm going to, is publishing each test score individually and the final score (of the year) won't be announced until the summer

### **Data Storage & Use**

at first, I started making a CSV file for each subject, but then I realized that other scores would be uploaded frequently and that it wasn't the best way to go
so using a spreadsheet was my best option so that I won't need to update files manually, but rather let the data get updated in the tool and collected using the API
once retrieved, I extracted the **data** list of lines containing the name and scores each, the **titles** list representing subjects that currently have at least one score submitted

**functions**
get_average(sid, weights) :
   :param sid: subject name
   :type  sid: str
   :param weights: subject weights
   :type  weights: Weights
   :raise ValueError: if sid is not in the titles list
   :return: subject's average score in class
   :rtype: float

get_score(first, last, sid) :
   :param first: student first name
   :type  first: str
   :param last: student last name
   :type  last: str
   :param sid: subject name
   :type  sid: str
   :raise ValueError: if student name is not available in the spreadsheet
   :return: subject's test scores
   :rtype: list of 3 floats


###**Data Structure**
starting up I pretty much made the right & final version of the Subject and Weights classes
but in the Student class I made the gradesbook a list of dictionaries, each including a Subject and its score which I didn't consider as the optimized way
taking into consideration the redundancy of the name, unit, and weights of each subject in all students, that is the same for all students
so I used each subject's name as a "primary key" in the gradesbook, and a list of scores (3 tests per subject) to optimize space complexity

**Classes**

class Weights:
   :att: float final
   :att: float midterm
   :att: float lab
   :raise ValueError: if the sum of atts is not 1 or a param is negative or zero

class Subject:
   :att: str name
   :att: str unit
   :att: float weight
   :att: Weights weights
   :raise ValueError: if weight is negative

   get_weights(self):
      :return: list of Weights
      :rtype: list of floats

class Student:
   :att: str first
   :att: str last
   :att: list(dict()) gradesbook: {"sid": subject_name "score": subject_score}
   :att: float full_potential_score
   :att: float proportional_score

   get_subject_score(self, sid):
      :param sid: subject name
      :type sid: str
      :raise ValueError: subject name is not in the gradesbook
      :return: weighted average of subject
      :rtype: float

   get_score(self, mode=None):
      :param mode: proportional or full_potential
      :type mode: str
      :return: student overall score
      :rtype: float


display(d, colored=None):
   :param d: list of lines to display
   :type d: list of str
   :param colored: display material color
   :type colored: bool
   :return: styled list on lines
   :rtyep: list of str

rank(user):
   :param user: student to find their rank
   :type user: Student
   :return: student ranking, list of higher ranking students
   :rtype: int, list of dict(): {"name": student_name, "score": student_score}
