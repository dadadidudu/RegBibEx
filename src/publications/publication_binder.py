from .bibtex import Bibtex
from ..binding.binder_options import BinderOptions
from ..binding.regex_variable_binder import RegexVariableBinder
from .publication import Publication
import os.path as path

class PublicationBinder:

	publication: Publication
	binder: RegexVariableBinder
	options: BinderOptions
	publications: list[Bibtex] = []

	def __init__(self, publication: Publication, options: BinderOptions):
		self.publication = publication
		self.options = options
		self.binder = RegexVariableBinder(binderoptions=options)
	
	def __get_options_for_file(self) -> dict[str,str] | None:
		filename = path.basename(self.publication.file)
		last_dot_idx = filename.rfind(".")
		filename = filename[0:last_dot_idx]
		opts_for_file = self.options.get_individual_options(filename)
		return opts_for_file

	def get_bibtex(self) -> list[Bibtex]:
		selector_pattern_map = self.__get_options_for_file()

		if selector_pattern_map is None:
			raise Exception("No selectors defined for " + self.publication.file)

		for selector in selector_pattern_map:
			if selector == "replace":
				continue

			pattern = selector_pattern_map.get(selector)

			texts_at_selector = self.publication.get_text_at(selector)

			for text in texts_at_selector:
				new_fields = self.__do_replaces_and_bind(text, pattern)
				if (len(new_fields) < 1):
					continue
				
				if (len(self.publications) > 0):
					# update newly created publication with existing fields (assumes all fields are in all publications)
					old_pub_to_update_new_from = self.publications[0]
					new_publication = Bibtex(old_pub_to_update_new_from.get_fields_and_values())
					new_publication.set_all_fields(new_fields)
				else:
					# create  a new publication
					new_publication = Bibtex(new_fields)

				# # update newly created publication with existing fields (assumes all fields are in all publications)
				# if (len(self.publications) > 0):
				# 	old_pub_to_update_new_from = self.publications[0]
				# 	for old_field in old_pub_to_update_new_from.get_current_fields():
				# 		old_value = new_publication.get_field_value(old_field)
				# 		if (old_value == ""):
				# 			new_publication.set_field(old_field, old_value)

				# update existing publications with new fields
				self.__update_existing_publications(new_fields)
				
				# add new publication to existing publications
				self.publications.append(new_publication)
			
			# now we should have every defined bibtex field
			pass
		
		return self.publications
				
	
	def __do_replaces_and_bind(self, bind_text: str, pattern: str) -> dict[str, str]:
		# do common replace (whitespace and options)
		bind_text = bind_text.replace("\n", " ")
		bind_text = bind_text.replace("\t", " ")
		bind_text = bind_text.replace("\r", " ")
		bind_text = bind_text.strip()
		global_replaces = self.options.options.get("replace")
		bind_text = self.__do_replaces(global_replaces, bind_text)

		# do publication specific replace (replace)
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
	
	def __update_existing_publications(self, new_fields: dict[str, str]):
		for pub in self.publications:
			pass


		# 	clone_and_insert_fields: list[str] = list(pub.keys())
		# 	for newfield in new_fields:
		# 		if newfield not in pub:
		# 			pub[newfield] = new_fields.get(newfield)
		# 		else:
		# 			clone_and_insert_fields.append(newfield)

		# 	# if (clone_and_insert_fields):
		# 	# 	cloned_pub = dict(pub)
		# 	# 	for field in new_fields:
		# 	# 		cloned_pub[field] = new_fields.get(field)
		# 	# 	new_publications.append(cloned_pub)

		# 	if len(clone_and_insert_fields) < 1:
		# 		continue

		# 	new_object: dict[str,str] = {}
		# 	for addfield in clone_and_insert_fields:
		# 		new_object[addfield] = pub[addfield]
		# 	for newfield in new_fields:
		# 		new_object[newfield] = pub[newfield]
		# 	new_publications.append(new_object)
			
		# self.publications.append(new_publications)
