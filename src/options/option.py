
class Option:
	"""
	The value(s) set for one option. Always supplied as a string.
	Setting an option value that doesn't already exist
	will add it to the list of options and mark this option as "is_multiple".
	Also supports a custom flag for whether this option set is a "is_add_key" option.
	"""

	is_multiple: bool
	is_add_key: bool
	__content: list[str]

	def __init__(self, option: str | list[str] = None):
		self.is_multiple = False
		self.is_add_key = False
		self.__content = []
		
		if (option is None):
			return
		
		if (isinstance(option, str)):
			self.set_option(option)
		else:
			for o in option:
				self.set_option(o)


	def set_option(self, new_or_added_option: str, is_add_key = False):
		self.__content.append(new_or_added_option)
		self.is_add_key = is_add_key
		if (len(self.__content) > 1):
			self.is_multiple = True
	
	def get_option(self) -> str | list[str]:
		if (self.is_multiple):
			return self.__content
		else:
			return self.__content[0]
