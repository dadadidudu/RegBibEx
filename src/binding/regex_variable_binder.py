import re
from .binder_options import BinderOptions

KEYWORD_VARIABLE_DEFINITION = " as " # {{REGEX as VARIABLE}}
valid_var_name = re.compile(r"([A-Za-z0-9_])+", re.S)

class RegexVariableBinder:
	"""
	Binds variables defined in RegularExpressions as python variables.
	E.g.: \\d.: {{TITLE}}, {{\\d{4} as YEAR}} will bind the contents of the string "1.: My Film Title, 1999" to the specified variables: TITLE: "My Film Title", YEAR: "1999".
	"""

	defaults: dict[str,str] = None
	variable_finder_pattern: re.Pattern

	def __init__(self, defaults: dict[str,str] = None, optionsfile: str = "", binderoptions: BinderOptions = None):
		"""
		Suppy either hardcoded defaults, a path to an options file for the binder, or already existing BinderOptions to be used for this Binder (in this priority).
		If none are supplied, only {{REGEX as VARIABLE}} definitions will work.
		"""

		if isinstance(defaults, dict):
			self.defaults = defaults
		elif defaults is not None:
			raise Exception("Passed default object is not a dictionary.")
		elif (optionsfile != ""):
			options = BinderOptions(optionsfile)
			self.defaults = options.defaults
		elif (binderoptions is not None):
			self.defaults = binderoptions.defaults
		else:
			print(r"RegexVariableBinder initialised without any options. Only {{REGEX as VARIABLE}} definitions possible.")

		self.variable_finder_pattern = re.compile(r"{{(.*?)}}") # finds {{VARIABLE}} and {{REGEX as VARIABLE}}
	
	def apply(self, string: str, regexes_with_bindings: list[str]) -> list[dict[str, str]]:
		"""
		Apply the given regex with bindings to the given string.
		Bindings can either be {{VAR_NAME}} or {{REGEX as VAR_NAME}}.
		For the former, the regex for VAR_NAME has been defined in the BindingOptions.defaults.
		The latter will override the default regex with the REGEX value.
			
			Parameters:
				string: the string to apply the regex to
				regex_with_bindings: the regex containing variable bindings as list
			
			Returns:
				A list of dictionaries where the requested variables have been bound to their value in the given input string. Each entry in the list corresponds to a regex. Each dictionary to the regex->variable mappings for the regex.
		"""

		all_mappings: list[dict[str, str]] = []

		for regex_with_bindings in regexes_with_bindings:
			
			# convert regex with bindings to a proper regex, saving occuring variables
			variables_present, proper_regex = self.__convert_binding_regex_to_common_regex(regex_with_bindings)
			
			# apply the converted regex
			r = self.__apply_regex(proper_regex, string)
			if (r is None):
				print(f"Regex {regex_with_bindings} yielded no results on string {string}")
				continue
			
			# generate return mapping
			mappings = self.__generate_mappings(r, variables_present)

			# add to results
			all_mappings.append(mappings)

		return all_mappings

	def __convert_binding_regex_to_common_regex(self, regex_to_convert: str) -> list[str]:
		""""
		Converts a regex string that includes bindings to a proper regex.
		Returns a tuple of 1. the list of the variable names that were found as bind targets, and 2. the proper regex.
		"""
		
		variables_present: list[str] = []
		common_regex = regex_to_convert

		# convert regex with bindings to a proper regex
		for varDef in re.findall(self.variable_finder_pattern, regex_to_convert):
			regex = ""
			variable = ""

			if (KEYWORD_VARIABLE_DEFINITION in varDef):
				# {{REGEX as VARIABLE}}
				split = varDef.split(KEYWORD_VARIABLE_DEFINITION, 2)
				regex = split[0]
				variable = split[1]
			else:
				# only {{VARIABLE}}
				if (self.defaults is not None):
					variable = varDef
					regex = self.defaults[varDef]
				else:
					raise Exception(r"Cannot use RegexVariableBinder with {{VARIABLE}} syntax: Defaults are missing.")

			if valid_var_name.search(variable) is None:
				raise Exception(f"Invalid variable name: {variable}. Variable name must be python compatible.")
			if regex is None:
				raise Exception(f"No regex definition for {variable} in defaults.")
			
			variables_present.append(variable)
			new = r"(?P<" + variable + ">" + regex + ")"
			common_regex = common_regex.replace(r"{{" + varDef + r"}}", new)
		
		return (variables_present, common_regex)

	def __apply_regex(self, regex: str, apply_to: str) -> re.Match[str] | None:
		compiled_regex = re.compile(regex, re.MULTILINE)
		r = re.search(compiled_regex, apply_to)
		return r


	def __generate_mappings(self, regex_result: re.Match, variables_present: list[str]) -> dict[str, str]:
		mappings: dict[str, str] = {}
		for varDef in variables_present:
			var_value = regex_result.group(varDef)
			mappings[varDef] = var_value
		return mappings
