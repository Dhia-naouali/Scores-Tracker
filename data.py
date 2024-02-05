from googleapiclient.discovery import build


"""
google sheets api:



installs:
pip install --upgrade google-api-python-client
"""


api_key = "AIzaSyBI5CoMHqTCCRZav8BsEJzI3d9TIiUJ1d0"
SPREAD_SHEET_ID = "1AKk3unx7a4d0Yq4CWi_8bD3It-E96LhRmx1wbaVrgDE"
spreadsheets = build("sheets", "v4", developerKey=api_key).spreadsheets()
data = spreadsheets.values().get(spreadsheetId=SPREAD_SHEET_ID, range="scores!A1:AZ").execute()

grades = data["values"][2:]
titles = [title.strip().lower() for title in data["values"][0] if title][1:]
MAX_TITLE_LEN = max(len(t) for t in titles)



def get_average(sid, weights):
    if sid in titles:
        n = titles.index(sid)
        candidates = []
        for row in grades:
            grade = 0
            for i in range(3):
                try:
                    grade += float(row[3*n + 2 + i]) * weights[i]
                except (IndexError, ValueError):
                    pass
            try:
                grade /= sum(weights[i] for i in range(3) if row[3*n + 2 + i])
            except (IndexError, ZeroDivisionError):
                pass
            candidates.append(grade)
        return round(float(sum(candidates) / len(candidates)), 2)
    else :
        raise ValueError("subject name typo")

def get_score(first, last, sid):
    if sid in titles:
        n = titles.index(sid)
        for row in grades:
            if row[0].strip().capitalize() == first.strip().capitalize() and row[1].strip().capitalize() == last.strip().capitalize():
                # found the student
                for subject in titles:
                    if subject.title() == sid.title():
                        # found the subject
                        score = []
                        for i in range(3):
                            try:
                                if s := row[3*n + 2 + i]:
                                    score.append(float(s))
                                else:
                                    score.append(0)
                            except IndexError:
                                score.append(0)
                        return score
        raise ValueError(f"student name : {first.capitalize().strip()} {last.capitalize().strip()} doesn't exist in the current database")
    return [0, 0, 0]
