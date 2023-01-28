import requests
from requests.exceptions import TooManyRedirects
from bs4 import BeautifulSoup
from datetime import date
import undetected_chromedriver as uc


class Chrome(uc.Chrome):
    def __del__(self) -> None:
        self.quit()


class User:
    def __init__(self, username, password):
        self.id = id
        self.username = username
        self.password = password
        self.courses = []


class Spider:
    def __init__(self, config) -> None:
        self.cuCookie = None
        self.currentIndex = None
        self.config = config

    def setCourse(self, course):
        url = f"https://cuonline.cuilahore.edu.pk:8091/Courses/SetCourse/{course}"
        headers = {"cookie": f"ASP.NET_SessionId={self.cuCookie}"}
        try:
            requests.get(url, headers=headers)
        except TooManyRedirects:
            self.currentIndex = course
            print(f"Index set to {self.currentIndex}")

    def getMarks(self):
        url = "https://cuonline.cuilahore.edu.pk:8091/MarksSummary/Index"
        headers = {"cookie": f"ASP.NET_SessionId={self.cuCookie}"}
        response = requests.get(url, headers=headers)
        soup = BeautifulSoup(response.content, "html.parser")
        return soup

    def __get_ChromeOptions(self):
        return (
            uc.ChromeOptions()
            .add_argument("--start_maximized")
            .add_argument("--disable-extensions")
            .add_argument("--disable-application-cache")
            .add_argument("--disable-gpu")
            .add_argument("--no-sandbox")
            .add_argument("--disable-setuid-sandbox")
            .add_argument("--disable-dev-shm-usage")
        )


class Course:
    def __init__(self, id, soup):
        self.id = id
        self.name = ""
        self.marks = []
        self.credits = 0
        self.assignments = []

    def extractMarks(self, soup):
        pass

    def extractAssignments(self, soup):
        pass

    def extractAttendance(self, soup):
        pass

    def extractGeneral(self, soup):
        return


class Marks:
    def __init__(self, name, obtained, total, _date):
        self.name = name
        self.obtained = obtained
        self.total = total
        self.date = date.fromisoformat(_date)


class Assignment:
    def __init__(self, name, uploaded, due, status):
        self.name = name
        self.uploaded = uploaded
        self.due = due
        self.status = status
