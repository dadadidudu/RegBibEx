
class Bibtex:

	__fields_and_values: dict[str, str] = {}

	def __init__(self, clone_from = None):
		if (clone_from is not None):
			self.__fields_and_values = dict(clone_from)
	
	def get_current_fields(self) -> set[str]:
		"Returns the list of fields in the Bibtex."
		return set(self.__fields_and_values.keys())
	
	def get_fields_and_values(self) -> dict[str, str]:
		return self.__fields_and_values

	def get_field_value(self, field_name: str) -> str:
		"Returns the string saved at the given field name, or empty string if nothing saved."
		return self.__fields_and_values.get(field_name, "")
	
	def set_field(self, field_name: str, field_entry: str) -> None:
		self.__fields_and_values[field_name] = field_entry

	def set_all_fields(self, field_name_and_entry_dict: dict[str, str]) -> None:
		for name, entry in field_name_and_entry_dict.items():
			self.set_field(name, entry)

	def has_all_fields_already(self, field_names: list[str]) -> bool:
		for fieldname in field_names:
			if (self.get_field_value(fieldname) == ""):
				return False
		return True