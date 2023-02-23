import asyncio
import os, json
import requests
from requests.exceptions import TooManyRedirects
from selenium import webdriver
from bs4 import BeautifulSoup
from datetime import date

import tls_client
import undetected_chromedriver as uc


class Chrome(uc.Chrome):
    def __del__(self) -> None:
        self.quit()


class User:
    def __init__(self, username: str, password: str):
        self.id = id
        self.username = username
        self.password = password
        self.courses = []


class Spider:
    """
    This class scrapes the data from all of
    the pages by injecting ASP.NetSession Cookie.
    """

    def __init__(self, aspCookie: str, verificationToken: str = None) -> None:
        self.currentIndex: str
        self.config: dict
        self.aspCookie = aspCookie
        self.verificationToken = verificationToken
        self.session = tls_client.Session(
            client_identifier="chrome_108",
        )

    def login(self):
        driver = Chrome(options=self.__getChromeOptions())
        webdriver.Chrome()

    async def setCourse(self, course):
        url = f"https://cuonline.cuilahore.edu.pk:8091/Courses/SetCourse/{course}"
        try:
            await requests.get(
                url, headers=self.__getHeaders(), cookies=self.__generateCookies()
            )
        except TooManyRedirects:
            self.currentIndex = course
            print(f"Index set to {self.currentIndex}")

    async def getMarks(self):
        url = "https://cuonline.cuilahore.edu.pk:8091/MarksSummary/Index"
        response = await requests.get(
            url, headers=self.__getHeaders(), cookies=self.__generateCookies()
        )
        soup = BeautifulSoup(response.content, "html.parser")
        return soup

    def __generateCookies(self):
        cookies = {"ASP.Net_SessionId": self.aspCookie}
        return (
            cookies
            if self.verificationToken is None
            else {**cookies, "__RequestVerificationToken": self.verificationToken}
        )

    def __getHeaders(self):
        # Include all headers to correctly mimic the request
        return {
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
            "Accept-Language": "en-US,en;q=0.9",
            "Cache-Control": "max-age=0",
            "Connection": "keep-alive",
            "Referer": "https://cuonline.cuilahore.edu.pk:8091/",
            "Sec-Fetch-Dest": "document",
            "Sec-Fetch-Mode": "navigate",
            "Sec-Fetch-Site": "same-origin",
            "Sec-Fetch-User": "?1",
            "Upgrade-Insecure-Requests": "1",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Safari/537.36",
            "sec-ch-ua": '^\\^"Not_A Brand^\\^";v=^\\^"99^\\^", ^\\^"Google Chrome^\\^";v=^\\^"109^\\^", ^\\^"Chromium^\\^";v=^\\^"109^\\^"',
            "sec-ch-ua-mobile": "?0",
            "sec-ch-ua-platform": '^\\^"Windows^\\^"',
        }

    def __getChromeOptions(self):
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
