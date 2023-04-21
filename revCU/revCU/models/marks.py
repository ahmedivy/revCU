from datetime import datetime


class Marks:
    def __init__(
        self,
        title=None,
        obtained=None,
        total=None,
        date=None,
        html=None,
    ):
        self.title = title
        self.obtained = obtained
        self.total = total
        self.date = date

        if html is not None:
            # Extract Marks
            title, obtained, total, date = html.find_all("td")
            self.title = str(title.text.strip())
            self.obtained = float(obtained.text.strip())
            self.total = float(total.text.strip())
            self.date = datetime.strptime(date.text.strip(), "%A, %d %B %Y").date()

    def __str__(self):
        return f"{self.title} - {self.obtained}/{self.total} - {self.date}"

    def to_json(self):
        return {
            "title": self.title,
            "obtained": self.obtained,
            "total": self.total,
            "date": self.date.strftime("%A, %d %B %Y"),
        }

    @classmethod
    def from_json(cls, json_dict: dict):
        return cls(
            title=json_dict.get("title"),
            obtained=json_dict.get("obtained"),
            total=json_dict.get("total"),
            date=datetime.strptime(json_dict.get("date"), "%A, %d %B %Y").date(),
        )
