from abc import ABC

OPTIONS_SECTION: str = "options"
DEFAULTS_SECTION: str = "defaults"
SECTION_DELIMITER: str = ":"
KEY_VALUE_SPLITTER: str = ":"
MULTIPLE_OPTION_OPEN: str = "["
MULTIPLE_OPTION_CLOSE: str = "]"

class AOptions(ABC):
	"""
	This class provides a standardised options definition in plaintext.
	The root objects 'options' and 'defaults' are defined by default.
	Furthermore, individual option objects can be defined by their own key.
	"""

	__is_handling_multiple_option: bool = False
	__last_key: str
	options: dict[str,str] = {}
	defaults: dict[str,str] = {}
	individual_opts: dict[str, dict[str, list[str]]] = {}

	def __init__(self, options_file: str):
		"""
		Parses the given options file.
			Parameters:
				options_file: the path to the option file
		"""

		option_lines: list[str]
		with open(options_file) as f:
			option_lines = f.readlines()
		current_section: str
		for oln in option_lines:
			oln = oln.strip()
			if (oln == (OPTIONS_SECTION + SECTION_DELIMITER)): # options:
				current_section = OPTIONS_SECTION
			elif (oln == (DEFAULTS_SECTION + SECTION_DELIMITER)): # defaults:
				current_section = DEFAULTS_SECTION
			elif (oln.endswith(SECTION_DELIMITER)): # indiv_opt:
				current_section = self.__new_individual_option__(oln)
			else: # option for current section
				self.__setoption__(current_section, oln)

	def __setoption__(self, current_section: str, line: str) -> None:
		"Sets the option in the currently selected option section. Raises error if no section was found."
		if (line.strip() == ""):
			return

		if (self.__is_handling_multiple_option):
			if (line.strip() == MULTIPLE_OPTION_CLOSE): # ]
				self.__is_handling_multiple_option = False
				return
			else: # multiple_option to set
				self.__set_individual_option_value(current_section, self.__last_key, line)
				return

		key, val = line.strip().split(KEY_VALUE_SPLITTER)
		
		if (val == MULTIPLE_OPTION_OPEN): # [
			self.__is_handling_multiple_option = True
			self.__last_key = key
			return
			
		
		if (current_section == OPTIONS_SECTION):
			self.options[key] = val
		elif (current_section == DEFAULTS_SECTION):
			self.defaults[key] = val
		elif (current_section in self.individual_opts):
			self.__set_individual_option_value(current_section, key, val)
		else:
			raise "No section found for " + line

	def __new_individual_option__(self, line: str) -> str:
		"Creates a new individual option section from the given option line and returns the name of the section."
		optionsection_name = line = line.replace(SECTION_DELIMITER, "")
		self.individual_opts[optionsection_name] = {}
		return optionsection_name
	
	def __set_individual_option_value(self, indiv_option_section: str, indiv_option_key: str, new_value: str):
		individual_section = self.get_individual_options(indiv_option_section)
		if (individual_section is None):
			self.individual_opts[individual_section] = {}
		exiting_options = individual_section.get(indiv_option_key, None)
		if (exiting_options is None):
			value_list = []
			value_list.append(new_value)
			self.individual_opts[indiv_option_section][indiv_option_key] = value_list
		else:
			self.individual_opts[indiv_option_section][indiv_option_key].append(new_value)
		

	def get_individual_options(self, key: str) -> dict[str, str] | None:
		"""
		Returns an object that is defined at the root of the options file in the form of:
		<KEY>:\\n\\t<INDIVIDUAL_KEY>:<VALUE>.
		Returns None if the key hasn't been defined.
		"""
		return self.individual_opts.get(key, None)
	
	def __check_and_add_multiple_option(self, current_section: str, current_line: str):
		if (self.__is_handling_multiple_option):
			if (current_line.strip() == MULTIPLE_OPTION_CLOSE):
				self.__is_handling_multiple_option = False
				return
			else:
				self.individual_opts[current_section][key].append(current_line)
				return

		key, val = current_line.strip().split(KEY_VALUE_SPLITTER)
		if (val == MULTIPLE_OPTION_OPEN):
			self.__is_handling_multiple_option = True
			return