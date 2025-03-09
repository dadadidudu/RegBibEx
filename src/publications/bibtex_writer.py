import os
import re
from ..binding.binder_options import BinderOptions
from .bibtex import Bibtex

ENTRYTYPE_OPTION_KEY = "entrytype"
DEFAULT_ENTRYTYPE_OPTION = "article"
CITEKEY_OPTION_KEY = "citekey"
DEFAULT_CITEKEY_OPTION = "title"
MAX_CITEKEY_LENGTH = 25

class BibtexWriter:
	
	__i = 0
	__directory: str
	__options: BinderOptions

	def __init__(self, directory: str, options: BinderOptions):
		self.__directory = directory
		self.__options = options

	def __get_bibtex_content(self, bibtex: Bibtex) -> str:
		content = "\n"
		for fld, val in bibtex.get_fields_and_values().items():
			content += f"\t{fld}\t=\t\"{val}\","
			content += "\n"
		return content
	
	def __get_entrytype(self, filename: str) -> str:
		default_entrytype = self.__options.defaults.get(ENTRYTYPE_OPTION_KEY, DEFAULT_ENTRYTYPE_OPTION)
		entrytype_for_this_file = self.__options.get_individual_options(filename).get_options(ENTRYTYPE_OPTION_KEY, default_entrytype)
		entrytype_value = entrytype_for_this_file.get_option()
		return entrytype_value

	def __get_citekey(self, filename: str, bibtex: Bibtex) -> str:
		default_citekey = self.__options.defaults.get(CITEKEY_OPTION_KEY, DEFAULT_CITEKEY_OPTION)
		citekey_for_this_file = self.__options.get_individual_options(filename).get_options(CITEKEY_OPTION_KEY, default_citekey)
		
		citekey_value: str = citekey_for_this_file.get_option()
		citekey_mapping = bibtex.get_field_value(citekey_value)
		
		if (citekey_mapping == ""):
			self.__i += 1
			return f"{DEFAULT_CITEKEY_OPTION}-{self.__i}"
		else:
			ignorechars = r"[^\w\d]"
			citekey_mapping = re.sub(ignorechars, "", citekey_mapping)
			citekey_mapping = citekey_mapping.replace(" ", "-")
			if (len(citekey_mapping) > MAX_CITEKEY_LENGTH):
				return citekey_mapping[0:MAX_CITEKEY_LENGTH]
			else:
				return citekey_mapping

	def write_bibtex_to_file(self, filename: str, file_content: list[Bibtex]):
		if (os.path.isdir(self.__directory) is False):
			os.makedirs(self.__directory)

		entrytype = self.__get_entrytype(filename)
		

		with open(f"{self.__directory}/{filename}.bibtex", mode="w", encoding="utf-8") as f:
			for btx in file_content:
				citekey = self.__get_citekey(filename, btx)
				f.write(f"""@{entrytype}{{{citekey},{self.__get_bibtex_content(btx)}}}\n""")