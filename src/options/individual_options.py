from .option import Option

ADD_PREFIX = "+"

class IndividualOptions:

	__options: dict[str, Option]
	is_add_key: bool

	def __init__(self):
		self.__options = {}
		self.is_add_key = False

	def add_option(self, key: str, value: str):
		existing = self.__options.get(key, None)
		if (existing is None):
			self.__options[key] = Option()
		self.__options[key].set_option(value)
	
	def get_options(self, key: str, default_value = None) -> Option | None:
		options = self.__options.get(key, default_value)
		return options
	
	def get_list(self) -> dict[str, Option]:
		return self.__options