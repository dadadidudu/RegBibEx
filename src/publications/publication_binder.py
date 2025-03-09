from .bibtex import Bibtex
from ..binding.binder_options import BinderOptions
from ..binding.regex_variable_binder import RegexVariableBinder
from .publication import Publication

REPLACE_OPTION = "replace"
ENTRYTYPE_OPTION = "entrytype"
CITEKY_OPTION = "citekey"
ADD_PREFIX = "+"

non_bibtex_field_options = [
	REPLACE_OPTION,
	ENTRYTYPE_OPTION,
	CITEKY_OPTION
]

class PublicationBinder:

	publication: Publication
	binder: RegexVariableBinder
	binder_opts: BinderOptions
	bibtex_list: list[Bibtex] = []

	def __init__(self, publication: Publication, options: BinderOptions):
		self.publication = publication
		self.binder_opts = options
		self.binder = RegexVariableBinder(binderoptions=options)
	
	def __get_options_for_file(self) -> dict[str, list[str]] | None:
		filename = self.publication.get_filename(with_extension=False)
		opts_for_file = self.binder_opts.get_individual_options(filename)
		return opts_for_file

	def get_bibtex(self) -> list[Bibtex]:
		selector_patterns_map = self.__get_options_for_file()

		if selector_patterns_map is None:
			raise Exception("No selectors defined for " + self.publication.get_filename(with_extension=False))

		fields_to_add_everywhere: list[Bibtex] = []

		for selector in selector_patterns_map:
			if selector.lower() in non_bibtex_field_options:
				continue # not a seletor

			pattern_entries = selector_patterns_map.get(selector)

			is_add = False
			if (selector.startswith(ADD_PREFIX)):
				selector = selector[1:]
				is_add = True
			
			texts_at_selector = self.publication.get_text_at(selector)

			for text in texts_at_selector:
				# each selector-text is a new bibtex or an addition to existing ones
				list_of_new_fields = self.__do_replaces_and_bind(text, pattern_entries)

				most_significat_fields = self.__get_most_significant_fields(list_of_new_fields)
				if (len(most_significat_fields) == 0):
					continue

				data_to_add = Bibtex(most_significat_fields)
				if (is_add):
					# add these fields to available data later on
					fields_to_add_everywhere.append(data_to_add)
				else:
					self.bibtex_list.append(data_to_add)
				
			# now we should have every defined bibtex field
			pass

		# add the fields that are universal to each bibtex
		for field_to_add_everywhere in fields_to_add_everywhere:
			for btx in self.bibtex_list:
				btx.set_all_fields(field_to_add_everywhere.get_fields_and_values())

		# self.__remove_duplicates_and_incompletes()
		return self.bibtex_list
				
	def __get_most_significant_fields(self, all_fields: list[dict[str, str]]) -> dict[str, str]:
		selected: dict[str, str] = {}
		if (all_fields is not None):
			for curr_fields in all_fields:
				# clear "None" entries
				only_defined_values: dict[str, str] = {}
				for (f, v) in curr_fields.items():
					if (v is not None and v != "None"):
						only_defined_values[f] = v
				# select "most significant", i.e. the one with the most bibtex entries
				if (len(only_defined_values) > len(selected)):
					selected = only_defined_values
		return selected

	def __do_replaces_and_bind(self, bind_text: str, patterns: list[str]) -> list[dict[str, str]]:
		# do common replace (whitespace characters)
		bind_text = bind_text.replace("\n", " ")
		bind_text = bind_text.replace("\t", " ")
		bind_text = bind_text.replace("\r", " ")
		bind_text = bind_text.strip()
		
		# do global replace (options.replace)
		global_replaces = self.binder_opts.options.get(REPLACE_OPTION)
		bind_text = self.__do_replaces(global_replaces, bind_text)

		# do publication specific replace (replace)
		file_specific_options = self.__get_options_for_file()
		if (REPLACE_OPTION in file_specific_options.keys()):
			specific_replaces = file_specific_options.get(REPLACE_OPTION)[0]
			bind_text = self.__do_replaces(specific_replaces, bind_text)

		# bind
		results = self.binder.apply(bind_text, patterns)
		if (len(results) == 0):
			print(f"No results found for patterns {patterns} in text {bind_text}")
			return {}
		else:
			return results

	def __do_replaces(self, options_string: str, text_to_replace_in: str) -> str:
		if options_string is not None:

			for replace_entry in options_string.split(",", 2):
				
				if replace_entry == "":
					continue

				replace_from_to = replace_entry.split("=", 2)
				text_to_replace_in = text_to_replace_in.replace(replace_from_to[0], replace_from_to[1])

		return text_to_replace_in
	
	def __remove_duplicates_and_incompletes(self):
		# incompletes
		all_current_fields = set()
		for b in self.bibtex_list:
			all_current_fields.update(b.get_current_fields())
		
		for b in self.bibtex_list:
			curr_fields = b.get_current_fields()
			if (all_current_fields != curr_fields):
				self.bibtex_list.remove(b)
		
		# duplicates
		for b in self.bibtex_list:
			for b2 in [entry for entry in self.bibtex_list if entry != b]:
				if (b.equals(b2)):
					self.bibtex_list.remove(b)
					break
