from .binding.binder_options import BinderOptions
from .binding.regex_variable_binder import RegexVariableBinder
from .journal import Journal
import os.path as path

class JournalBinder:

	journal: Journal
	binder: RegexVariableBinder
	options: BinderOptions

	def __init__(self, journal: Journal, options: BinderOptions):
		self.journal = journal
		self.options = options
		self.binder = RegexVariableBinder(binderoptions=options)
	
	def __get_options_for_file(self) -> dict[str,str] | None:
		filename = path.basename(self.journal.file)
		last_dot_idx = filename.rfind(".")
		filename = filename[0:last_dot_idx]
		opts_for_file = self.options.get_individual_options(filename)
		return opts_for_file

	def get_bibtex(self):
		selector_pattern_map = self.__get_options_for_file()

		if selector_pattern_map is None:
			raise Exception("No selectors defined for " + self.journal.file)
		
		fields: dict[str, str] = {}

		for selector in selector_pattern_map:
			if selector == "replace":
				continue

			pattern = selector_pattern_map.get(selector)

			texts_at_selector = self.journal.get_text_at(selector)

			for text in texts_at_selector:
				bound_fields = self.__do_replaces_and_bind(text, pattern)
				fields.update(bound_fields)
			
			# now we should have every defined bibtex field
			pass
		pass
				
	
	def __do_replaces_and_bind(self, bind_text: str, pattern: str) -> dict[str, str]:
		# do common replace (options)
		global_replaces = self.options.options.get("replace")
		bind_text = self.__do_replaces(global_replaces, bind_text)

		# do journal specific replace (replace)
		specific_replaces = self.__get_options_for_file().get("replace")
		bind_text = self.__do_replaces(specific_replaces, bind_text)

		# bind
		results = self.binder.apply(bind_text, pattern)
		if (results is None):
			print(f"No results found for pattern {pattern} in text {bind_text}")
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
				pass
		return text_to_replace_in