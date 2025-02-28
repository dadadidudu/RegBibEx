import bs4
from os import path

class Journal:

    file: str
    raw_journal: bs4.BeautifulSoup = None

    def __init__(self, journal_file: str):
        self.file = journal_file
        with open(journal_file, "r", encoding="cp1252") as file:
            content = file.read()
            self.raw_journal = bs4.BeautifulSoup(content, features="lxml")

    def as_htmltext(self, pretty=True) -> str:
        return self.raw_journal.decode(pretty, "cp1252")

    def as_plaintext(self) -> str:
        return self.raw_journal.get_text()
    
    def write_to_file(self, filename, pretty=True) -> None:
        '''
        Writes the journal to a file as converterd unicode with the given path, name and extension. Optionally pretty prints the HTML.
        '''
        with open(f"{filename}", "w", encoding="utf-8") as f:
            f.write(self.as_htmltext(pretty))

    def get_text_at(self, html_selector: str) -> list[str]:
        "Returns a list of the strings at the given html tag locations, split by a dot, starting from html.body."

        tags = html_selector.split(".")
        first_tag = tags.pop(0)
        resultset = self.raw_journal.html.body.find_all(first_tag)
        
        while len(tags) > 0:
            tag = tags.pop(0)
            resultset_for_tag: list[bs4.ResultSet] = []
            for rs in resultset:
                resultset_for_tag.extend(rs.find_all(tag))
            resultset = resultset_for_tag
        resulttext: list[str] = []
        for rs in resultset:
            text = rs.get_text(strip=True)
            resulttext.append(text)
        return resulttext
