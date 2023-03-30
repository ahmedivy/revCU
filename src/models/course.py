from enum import Enum


class Course:
    """
    This class represents a course.
    """

    # Course Types
    class Type(Enum):
        THEORY = 1
        PRACTICAL = 2

    def __init__(self, html=None):
        if html is None:
            raise Exception("No HTML provided")

        # Extract ID
        self.id = int(html["onclick"].split("/")[-1].strip("'"))

        # Extract General
        code, course, credits, professor, _, attendance = html.find_all("td")
        self.code = code.text.strip()
        self.name = course.text.strip()
        self.credit = int(credits.text.strip())
        self.professor = professor.text.strip()
        self.type = (
            self.Type.THEORY
            if course["title"] == "Theory Only Scheme Course"
            else self.Type.PRACTICAL
        )

        # Extract Attendance
        self.attendance = {}
        theory = attendance.find("div", {"title": "Class Attendance"})
        self.attendance["theory"] = int(theory.get("aria-valuenow")) if theory else 0
        if self.type == self.Type.PRACTICAL:
            lab = attendance.find("div", {"title": "Lab Attendance"})
            self.attendance["practical"] = int(lab.get("aria-valuenow")) if lab else 0

        # Set Marks to None
        self.marks = []

    def __str__(self):
        return f"{self.code} - {self.name}"

    def set_marks(self, marks: list):
        self.marks = marks
