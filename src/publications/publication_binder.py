from .bibtex import Bibtex
from ..binding.binder_options import BinderOptions
from ..binding.regex_variable_binder import RegexVariableBinder
from .publication import Publication

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
	
	def __get_options_for_file(self) -> dict[str,str] | None:
		filename = self.publication.get_filename(with_extension=False)
		opts_for_file = self.binder_opts.get_individual_options(filename)
		return opts_for_file

	def get_bibtex(self) -> list[Bibtex]:
		selector_pattern_map = self.__get_options_for_file()

		if selector_pattern_map is None:
			raise Exception("No selectors defined for " + self.publication.get_filename(with_extension=False))

		for selector in selector_pattern_map:
			if selector.lower() in non_bibtex_field_options:
				continue

			pattern_entry = selector_pattern_map.get(selector)

			texts_at_selector = self.publication.get_text_at(selector)

			for text in texts_at_selector:
				# each selector-text is a new bibtex or an addition to existing ones
				list_of_new_fields = self.__do_replaces_and_bind(text, pattern_entry)
				# every entry in this list is a bound object with data key/values

				for new_fields in list_of_new_fields:
					if (len(new_fields) < 1):
						continue

					new_publication: Bibtex = None
					
					if (len(self.bibtex_list) > 0):
						# update newly created publication with existing fields (assumes all fields are in all publications)
						old_pub_to_update_new_from = self.bibtex_list[0]
						new_publication = Bibtex(old_pub_to_update_new_from.get_fields_and_values())
						new_publication.set_all_fields(new_fields)

					else:
						# create  a new publication
						new_publication = Bibtex(new_fields)
					
					# add new publication to existing publications
					self.bibtex_list.append(new_publication)
			
			# now we should have every defined bibtex field
			pass

		self.__remove_duplicates_and_incompletes()
		return self.bibtex_list
				
	
	def __do_replaces_and_bind(self, bind_text: str, pattern: str) -> list[dict[str, str]]:
		# do common replace (whitespace characters)
		bind_text = bind_text.replace("\n", " ")
		bind_text = bind_text.replace("\t", " ")
		bind_text = bind_text.replace("\r", " ")
		bind_text = bind_text.strip()
		
		# do global replace (options.replace)
		global_replaces = self.binder_opts.options.get("replace")
		bind_text = self.__do_replaces(global_replaces, bind_text)

		# do publication specific replace (replace)
		specific_replaces = self.__get_options_for_file().get("replace")
		bind_text = self.__do_replaces(specific_replaces, bind_text)

		# bind
		results = self.binder.apply(bind_text, pattern)
		if (len(results) == 0):
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
