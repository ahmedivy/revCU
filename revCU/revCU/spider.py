import os
import re
import json
import dotenv
import logging
import requests

from bs4 import BeautifulSoup
from requests.exceptions import TooManyRedirects
from playwright.sync_api import sync_playwright

from .models import Course, Marks


BASE_URL = "https://cuonline.cuilahore.edu.pk:8091/"
FILES_PATH = os.path.join(os.path.expanduser("~"), ".revCU")

dotenv.load_dotenv()


class Spider:
    """
    This class scrapes the data from all of
    the pages by injecting ASP.NetSession Cookie.
    """

    def __init__(self):
        self.config = self.read_config()
        self.cookies = dict
        self.session = requests.Session()
        self.courses = []

    def read_config(self):
        path = os.path.join(FILES_PATH, "config.json")
        if not os.path.exists(FILES_PATH):
            os.mkdir(FILES_PATH)
        if not os.path.exists(path):
            return {}
        with open(path) as f:
            return json.load(f)

    def write_config(self):
        path = os.path.join(FILES_PATH, "config.json")
        with open(path, "w") as f:
            json.dump(self.config, f, indent=4)

    def read_marks(self):
        path = os.path.join(FILES_PATH, "marks.json")
        if not os.path.exists(path):
            pass
        with open(path) as f:
            temp = json.load(f)
            for course in temp["courses"]:
                self.courses.append(Course.from_json(course))

    def set_course(self, course_id: int):
        """
        Sets the current course to the given course id.

        Args:
            course_id (int): Course ID
        """

        try:
            self.session.get(f"{BASE_URL}Courses/SetCourse/{course_id}")
        except TooManyRedirects:
            pass

    def get_marks(self) -> list:
        """
        Returns a list of marks for current Indexed Course.

        Returns:
            list: List of Marks objects
        """

        response = self.session.get(f"{BASE_URL}MarksSummary/Index")
        soup = BeautifulSoup(response.content, "html.parser")
        marks_list = []
        for body in soup.find_all("tbody"):
            for row in body.find_all("tr"):
                marks = Marks(html=row)
                marks_list.append(marks)
        return marks_list

    def scrape_dashboard(self):
        """
        Scrapes the dashboard page and extracts all the courses names.
        """
        response = self.session.get(f"{BASE_URL}Courses/Index")
        soup = BeautifulSoup(response.content, "html.parser")
        for row in soup.find("tbody").find_all("tr"):
            course = Course(row)
            self.courses.append(course)

    def get_cookies(self):
        """
        Gets the ASP.NET_SessionId cookie from the browser.
        """
        with sync_playwright() as p:
            # Launch browser and go to the base url
            browser = p.chromium.launch(headless=False)
            page = browser.new_page()
            logging.info("Launched Chromium")

            # Go to base url
            page.goto(BASE_URL)
            logging.info("Navigated to base url")

            # Login
            page.locator(".close").click()
            page.locator("#MaskedRegNo").type(os.getenv("REG_NO"))
            page.locator("#Password").type(os.getenv("PASSWORD"))
            self.solve_recaptcha(page.frame(url=re.compile("recaptcha")))
            page.click('button:has-text("Login")')
            logging.debug("Logged in")

            # Get ASP.NET_SessionId cookie
            page.wait_for_load_state("networkidle")
            cookies = page.context.cookies()
            asp_cookie = next(
                (cookie for cookie in cookies if cookie["name"] == "ASP.NET_SessionId"),
                None,
            )
            if asp_cookie:
                logging.info("Cookie Found")
                self.cookies = {asp_cookie["name"]: asp_cookie["value"]}
                self.session.cookies.update(self.cookies)
            browser.close()
            logging.info("Closed Browser")

    def solve_recaptcha(self, frame):
        """
        Waits until user solves the recaptcha.
        """
        frame.locator("#recaptcha-anchor-label").click()
        frame.wait_for_function(
            '() => document.querySelector("#recaptcha-accessible-status")'
            '.textContent.includes("You are verified")'
        )
        logging.info("Recaptcha solved")

    def generate_marks(self):
        """
        Generates the marks for all the courses
        by sending a request to the server one by one
        by injecting the ASP.NET_SessionId cookie.
        """
        for course in self.courses:
            self.set_course(course.id)
            course.set_marks(self.get_marks())
            yield course

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        return self.session.close()
