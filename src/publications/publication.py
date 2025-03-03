from os import path
import bs4

class Publication:

    __file: str
    __encoding: str
    __raw_publication: bs4.BeautifulSoup = None

    def __init__(self, publication_file: str, encoding: str = None):
        self.__file = publication_file
        self.__encoding = encoding
        with open(publication_file, "r", encoding=self.__encoding) as f:
            content = f.read()
            self.__raw_publication = bs4.BeautifulSoup(content, features="lxml")

    def get_filename(self, with_extension: bool = True) -> str:
        if (with_extension):
            return path.basename(self.__file)
        else:
            name = path.basename(self.__file)
            return name[0 : name.rfind(".")]


    def as_htmltext(self, pretty=True) -> str:
        return self.__raw_publication.decode(pretty, self.__encoding)

    def as_plaintext(self) -> str:
        return self.__raw_publication.get_text()
    
    def write_to_file(self, filename, pretty=True) -> None:
        '''
        Writes the publication to a file as converterd unicode with the given path, name and extension. Optionally pretty prints the HTML.
        '''
        with open(f"{filename}", "w", encoding="utf-8") as f:
            f.write(self.as_htmltext(pretty))

    def get_text_at(self, html_selector: str) -> list[str]:
        "Returns a list of the strings at the given html tag locations, split by a dot, starting from html.body."

        tags = html_selector.split(".")
        first_tag = tags.pop(0)
        resultset = self.__raw_publication.html.body.find_all(first_tag)
        
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
