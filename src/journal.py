import bs4
from os import path


class Journal:

    raw_journal: bs4.BeautifulSoup = None

    def __init__(self, jorunal_file: str):
        pth = path.join(jorunal_file)
        with open(pth, "r", encoding="cp1252") as file:
            content = file.read()
            self.raw_journal = bs4.BeautifulSoup(content, features="lxml")

    def as_htmltext(self):
        return self.raw_journal.decode(False, "cp1252")

    def as_plaintext(self):
        return self.raw_journal.get_text()
