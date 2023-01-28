import requests
from bs4 import BeautifulSoup
from datetime import datetime, date


class User():
    
    def __init__(self, username, password):
        self.id = id
        self.username = username
        self.password = password
        self.courses = []
              
    
class Bot:

    def __init__(self):
        self.cuCookie = None
        self.currentIndex = None
        
    def setCourse(self, course):
        url = f'https://cuonline.cuilahore.edu.pk:8091/Courses/SetCourse/{course}'
        headers = {"cookie": f'ASP.NET_SessionId={self.cuCookie}'}
        try:
            requests.get(url, headers=headers)
        except requests.TooManyRedirects:
            pass
        finally:
            self.currentIndex = course
        print(f'Index set to {self.currentIndex}')
            
    def getMarks(self):
        url = "https://cuonline.cuilahore.edu.pk:8091/MarksSummary/Index"
        headers = {"cookie": f'ASP.NET_SessionId={cookie}'}
        response = requests.get(url, headers=headers)
        soup = BeautifulSoup(response.content, "html.parser")
        return soup

        

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
        
