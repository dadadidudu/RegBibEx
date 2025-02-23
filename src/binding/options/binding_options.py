OPTIONS_SECTION: str = "options"
DEFAULTS_SECTION: str = "defaults"
SECTION_DELIMITER: str = ":"
KEY_VALUE_SPLITTER: str = ":"

class BindingOptions:

	options: dict[str,str] = {}
	defaults: dict[str,str] = {}
	individual_opts: dict[str, dict[str, str]] = {}

	def __init__(self, options_file: str):
		option_lines: list[str]
		with open(options_file) as f:
			option_lines = f.readlines()
		current_section: str
		for oln in option_lines:
			oln = oln.strip()
			if (oln == (OPTIONS_SECTION + SECTION_DELIMITER)):
				current_section = OPTIONS_SECTION
			elif (oln == (DEFAULTS_SECTION + SECTION_DELIMITER)):
				current_section = DEFAULTS_SECTION
			elif (oln.endswith(SECTION_DELIMITER)):
				current_section = self.__new_individual_option__(oln)
			else:
				self.__setoption__(current_section, oln)

	def __setoption__(self, current_section: str, line: str) -> None:
		"Sets the option in the currently selected option section. Raises error if no section was found."
		key, val = line.strip().split(KEY_VALUE_SPLITTER)
		if (current_section == OPTIONS_SECTION):
			self.options[key] = val
		elif (current_section == DEFAULTS_SECTION):
			self.defaults[key] = val
		elif (current_section in self.individual_opts):
			self.individual_opts[current_section][key] = val
		else:
			raise "No section found for " + line

	def __new_individual_option__(self, line: str) -> str:
		"Creates a new individual option section from the given option line and returns the name of the section."
		optionsection_name = line = line.replace(SECTION_DELIMITER, "")
		self.individual_opts[optionsection_name] = {}
		return optionsection_name
	
	def get_options_for(self, index: str) -> dict[str, str]:
		return self.individual_opts[index]