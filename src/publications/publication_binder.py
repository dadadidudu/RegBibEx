from .bibtex import Bibtex
from ..binding.binder_options import BinderOptions
from ..binding.regex_variable_binder import RegexVariableBinder
from .publication import Publication
from ..options.individual_options import IndividualOptions
from ..options.option import Option

non_bibtex_field_options = [
	"replace",
	"entrytype",
	"citekey",
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
	
	def __get_options_for_file(self) -> IndividualOptions | None:
		filename = self.publication.get_filename(with_extension=False)
		opts_for_file = self.binder_opts.get_individual_options(filename)
		return opts_for_file

	def get_bibtex(self) -> list[Bibtex]:
		file_options = self.__get_options_for_file()
		fields_to_add_to_all_later: list[dict[str, str]] = []

		if file_options is None:
			raise Exception("No selectors defined for " + self.publication.get_filename(with_extension=False))

		for option_entry in file_options.get_list():
			if option_entry.lower() in non_bibtex_field_options:
				continue

			html_selector = option_entry
			selector_options = file_options.get_options(html_selector)
			texts_at_selector = self.publication.get_text_at(html_selector)

			for text in texts_at_selector:
				new_fields = self.__do_replaces_and_bind(text, selector_options)

				if (new_fields is None or len(new_fields) < 1):
					continue # no bound fields for this selector-regex entry

				if (selector_options.is_add_key):
					fields_to_add_to_all_later.append(new_fields)
				else:
					# create  a new publication
					new_publication: Bibtex = self.__create_new_bibtex_for_fields(new_fields)
					# add new publication to existing publications
					self.bibtex_list.append(new_publication)
			
			# now we should have every defined bibtex field
			pass

		# add collected fields to add all
		for f in fields_to_add_to_all_later:
			self.__add_binding_to_all_existing_bibtex(f)
		
		# TODO might not be needed?
		#self.__remove_duplicates_and_incompletes()
		return self.bibtex_list
				
	
	def __do_replaces_and_bind(self, bind_text: str, patterns_option: Option) -> dict[str, str]:
		# do common replace (whitespace characters)
		bind_text = bind_text.replace("\n", " ")
		bind_text = bind_text.replace("\t", " ")
		bind_text = bind_text.replace("\r", " ")
		bind_text = bind_text.strip()
		
		# do global replace (options.replace)
		global_replaces = self.binder_opts.options.get("replace")
		bind_text = self.__do_replaces(global_replaces, bind_text)

		# do publication specific replace (replace)
		file_options = self.__get_options_for_file()
		specific_replace_options = file_options.get_options("replace")
		if (specific_replace_options is not None):
			bind_text = self.__do_replaces(specific_replace_options, bind_text)

		bind_result = self.__do_bind(bind_text, patterns_option)
		return bind_result

	def __do_replaces(self, replace_option: Option, text_to_replace_in: str) -> str:
		replaces: list[str]
		if (replace_option.is_multiple):
			replaces = replace_option.get_option()
		else:
			replaces = replace_option.get_option().split(",", 2)

		for replace_entry in replaces:
			
			if replace_entry is None or replace_entry == "":
				continue

			replace_from_to = replace_entry.split("=", 2)
			text_to_replace_in = text_to_replace_in.replace(replace_from_to[0], replace_from_to[1])

		return text_to_replace_in
	
	def __do_bind(self, bind_text: str, patterns_option: Option) -> dict[str, str]:
		bind_result: dict[str, str]
		
		if (patterns_option.is_multiple):
			patterns: list[str] = patterns_option.get_option()
			all_results: list[dict[str, str]] = []
			for pat in patterns:
				this_result = self.binder.apply(bind_text, pat)
				if (this_result is not None):
					this_result = self.__remove_invalid_entries(this_result)
					all_results.append(this_result)
			bind_result = self.__find_most_plausible_result(all_results)
		else:
			pattern: str = patterns_option.get_option()
			bind_result = self.binder.apply(bind_text, pattern)
			bind_result = self.__remove_invalid_entries(bind_result)
		return bind_result
	
	def __find_most_plausible_result(self, all_results: list[dict[str, str]]) -> dict[str, str]:
		most_plausible_result: dict[str, str] = {}
		for result in all_results:
			if (len(result) > len(most_plausible_result)):
				most_plausible_result = result
		return most_plausible_result
	
	def __remove_invalid_entries(self, entries: dict[str, str]) -> dict[str, str]:
		for k in list(entries.keys()):
			if (entries[k] is None or entries[k] == str(None)):
				del entries[k]
		return entries

	
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

	def __add_binding_to_all_existing_bibtex(self, fields_to_add: dict[str, str]):
		for b in self.bibtex_list:
			b.set_all_fields(fields_to_add)
	
	def __create_new_bibtex_for_fields(self, fields_for_new_bibtex: dict[str, str]) -> Bibtex:
		new_bibtex = Bibtex()
		new_bibtex.set_all_fields(fields_for_new_bibtex)
		return new_bibtex