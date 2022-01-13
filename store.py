import datetime

class Newsletter():
    def __init__(self, created: datetime.date, subject: str, body: str = None):
        self.created = created
        self.subject = subject
        self.body = body

def get_newsletters():
    result = []
    result.append(Newsletter(created=datetime.date(2022, 1, 12), subject="My first newsletter", body="""
Line 1
Line 2
Line 3
"""))
    result.append(Newsletter(created=datetime.date(2022, 1, 14), subject="News, news, news!"))

    for n in range(50):
        result.append(Newsletter(created=datetime.date(2022, 1, 15), subject=f"This is a test newsletter {n}"))

    return result