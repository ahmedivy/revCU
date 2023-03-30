from datetime import date


class Marks:
    def __init__(self, html=None):
        if html is None:
            raise Exception("No HTML provided")

        # Extract Marks
        title, obtained, total, _date = html.find_all("td")
        self.title = title.text.strip()
        self.obtained = int(obtained.text.strip())
        self.total = int(total.text.strip())
        self.date = date.fromisoformat(_date.text.strip())

    def __str__(self):
        return f"{self.title} - {self.obtained}/{self.total} - {self.date}"
