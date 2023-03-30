from datetime import datetime


class Marks:
    def __init__(self, html=None):
        if html is None:
            raise Exception("No HTML provided")

        # Extract Marks
        title, obtained, total, date = html.find_all("td")
        self.title = title.text.strip()
        self.obtained = float(obtained.text.strip())
        self.total = float(total.text.strip())
        self.date = datetime.strptime(date.text.strip(), "%A, %d %B %Y").date()

    def __str__(self):
        return f"{self.title} - {self.obtained}/{self.total} - {self.date}"
