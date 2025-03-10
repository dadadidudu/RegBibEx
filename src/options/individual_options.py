from .option import Option

ADD_PREFIX = "+"

class IndividualOptions:

	__options: dict[str, Option]

	def __init__(self):
		self.__options = {}

	def add_option(self, key: str, value: str):
		key_is_add = False

		if (key.startswith(ADD_PREFIX)):
			key = key[1:]
			key_is_add = True

		existing = self.__options.get(key, None)

		if (existing is None):
			self.__options[key] = Option()

		self.__options[key].set_option(value, key_is_add)
	
	def get_options(self, key: str, default_value = None) -> Option | None:
		options = self.__options.get(key, default_value)
		return options
	
	def get_list(self) -> dict[str, Option]:
		return self.__options