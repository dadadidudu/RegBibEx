from os import path
import bs4

class Publication:
    """
    A container for one HTML file (publication).
    Uses BeautifulSoup4 to parse the given HTML file and provide easy access to the text inside.
    """

    __file: str
    __input_encoding: str
    __raw_publication: bs4.BeautifulSoup

    def __init__(self, publication_file: str, input_encoding: str = None):
        self.__file = publication_file
        self.__input_encoding = input_encoding
        with open(publication_file, "r", encoding=self.__input_encoding) as f:
            content = f.read()
            self.__raw_publication = bs4.BeautifulSoup(content, features="lxml")

    def get_filename(self, with_extension: bool = True) -> str:
        if (with_extension):
            return path.basename(self.__file)
        else:
            name = path.basename(self.__file)
            return name[0 : name.rfind(".")]


    def as_htmltext(self, pretty=True, out_encoding:str=None) -> str:
        return self.__raw_publication.decode(pretty, out_encoding)

    def as_plaintext(self) -> str:
        return self.__raw_publication.get_text()
    
    def write_to_file(self, filename, pretty=True, out_encoding: str = None) -> None:
        '''
        Writes the publication to a file as converterd unicode with the given path, name and extension. Optionally pretty prints the HTML.
        '''
        with open(f"{filename}", "w", encoding=out_encoding) as f:
            f.write(self.as_htmltext(pretty, out_encoding))

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
