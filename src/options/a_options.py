from abc import ABC
from .individual_options import IndividualOptions
from .option import Option

OPTIONS_SECTION: str = "options"
DEFAULTS_SECTION: str = "defaults"
SECTION_DELIMITER: str = ":"
KEY_VALUE_SPLITTER: str = ":"

class AOptions(ABC):
	"""
	This class provides a standardised options definition in plaintext.
	The root objects 'options' and 'defaults' are defined by default.
	Furthermore, individual option objects can be defined by their own key.
	"""

	options: dict[str, Option]
	defaults: dict[str, Option]
	individual_opts: dict[str, IndividualOptions]

	def __init__(self, options_file: str):
		"""
		Parses the given options file.
			Parameters:
				options_file: the path to the option file
		"""
		self.options = {}
		self.defaults = {}
		self.individual_opts = {}

		option_lines: list[str]
		with open(options_file, encoding="utf-8") as f:
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
			self.options[key] = Option(val)
		elif (current_section == DEFAULTS_SECTION):
			self.defaults[key] = Option(val)
		elif (current_section in self.individual_opts):
			self.individual_opts[current_section].add_option(key, val)
		else:
			raise "No section found for " + line

	def __new_individual_option__(self, line: str) -> str:
		"Creates a new individual option section from the given option line and returns the name of the section."
		optionsection_name = line = line.replace(SECTION_DELIMITER, "")
		self.individual_opts[optionsection_name] = IndividualOptions()
		return optionsection_name
	
	def get_individual_options(self, key: str) -> IndividualOptions | None:
		"""
		Returns an object that is defined at the root of the options file in the form of:
		<KEY>:\\n\\t<INDIVIDUAL_KEY>:<VALUE>.
		Returns None if the key hasn't been defined.
		"""
		return self.individual_opts.get(key, None)