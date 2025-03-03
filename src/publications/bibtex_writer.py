import os
from ..binding.binder_options import BinderOptions
from .bibtex import Bibtex


class BibtexWriter:
	
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
	
	def __get_entrytype(self) -> str:
		return "article"

	def __get_citekey(self) -> str:
		return "cite1"

	def write_bibtex_to_file(self, filename: str, file_content: list[Bibtex]):
		if (os.path.isdir(self.__directory) is False):
			os.makedirs(self.__directory)

		entrytype = self.__get_entrytype()
		citekey = self.__get_citekey()

		with open(f"{self.__directory}/{filename}.bibtex", mode="w") as f:
			for btx in file_content:
				f.write(f"""@{entrytype}{{{citekey},{self.__get_bibtex_content(btx)}}}\n""")