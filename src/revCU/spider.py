import os
import re
import dotenv
import logging
import requests

from bs4 import BeautifulSoup
from requests.exceptions import TooManyRedirects
from playwright.async_api import async_playwright

from .models import Course, Marks


BASE_URL = "https://cuonline.cuilahore.edu.pk:8091/"

dotenv.load_dotenv()


class Spider:
    """
    This class scrapes the data from all of
    the pages by injecting ASP.NetSession Cookie.
    """

    def __init__(self):
        self.config: dict
        self.cookies = dict
        self.session = requests.Session()
        self.courses = []

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
                marks = Marks(row)
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

    async def get_cookies(self):
        """
        Gets the ASP.NET_SessionId cookie from the browser.
        """
        async with async_playwright() as p:
            # Launch browser and go to the base url
            browser = await p.chromium.launch(headless=False)
            page = await browser.new_page()
            logging.info("Launched Chromium")

            # Go to base url
            await page.goto(BASE_URL)
            logging.info("Navigated to base url")

            # Login
            await page.locator(".close").click()
            await page.locator("#MaskedRegNo").type(os.getenv("REG_NO"))
            await page.locator("#Password").type(os.getenv("PASSWORD"))
            await self.solve_recaptcha(page.frame(url=re.compile("recaptcha")))
            await page.click('button:has-text("Login")')
            logging.debug("Logged in")

            # Get ASP.NET_SessionId cookie
            await page.wait_for_load_state("networkidle")
            cookies = await page.context.cookies()
            asp_cookie = next(
                (cookie for cookie in cookies if cookie["name"] == "ASP.NET_SessionId"),
                None,
            )
            if asp_cookie:
                logging.info("Cookie Found")
                self.cookies = {asp_cookie["name"]: asp_cookie["value"]}
                self.session.cookies.update(self.cookies)
            await browser.close()
            logging.info("Closed Browser")

    async def solve_recaptcha(self, frame):
        """
        Waits until user solves the recaptcha.
        """
        await frame.locator("#recaptcha-anchor-label").click()
        await frame.wait_for_function(
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

    async def __aenter__(self):
        await self.get_cookies()
        return self

    async def __aexit__(self, exc_type, exc_value, traceback):
        return self.session.close()
