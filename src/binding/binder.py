import re
from .binder_options import BinderOptions

KEYWORD_VARIABLE_DEFINITION = " as " # REGEX as VARIABLE

class Binder:

	options: BinderOptions
	variables: dict[str, str]
	variable_finder_pattern: re.Pattern

	def __init__(self, optionsfile: str):
		self.options = BinderOptions(optionsfile)
		self.variable_finder_pattern = re.compile(r"{{(.*?)}}") # finds {{VARIABLE}} and {{REGEX as VARIABLE}}
	
	def apply(self, string: str, regex_with_bindings: str) -> dict[str, str]:
		"""
		Apply the given regex with bindings to the given string.
		Bindings can either be {{VAR_NAME}} or {{REGEX as VAR_NAME}}.
		For the former, the regex for VAR_NAME has been defined in the BindingOptions.defaults.
		The latter will override the default regex with the REGEX value.
			Parameters:
				string: the string to apply the regex to
				regex_with_bindings: the regex containing variable bindings
			Returns:
				A dictionary where the requested variables have been bound to their value in the given input string.
		"""
		variables_present: list[str] = []

		# convert regex with bindings to a proper regex
		for var in re.findall(self.variable_finder_pattern, regex_with_bindings):
			regex = ""
			variable = ""

			if (KEYWORD_VARIABLE_DEFINITION in var):
				# {{REGEX as VARIABLE}}
				split = var.split(KEYWORD_VARIABLE_DEFINITION, 2)
				regex = split[0]
				variable = split[1]
			else:
				# only {{VARIABLE}}
				variable = var
				regex = self.options.defaults[var]

			variables_present.append(variable)
			new = r"(?P<" + variable + ">" + regex + ")"
			regex_with_bindings = regex_with_bindings.replace(r"{{" + var + r"}}", new)
		
		# aapply the converted regex
		compiled_regex = re.compile(regex_with_bindings, re.MULTILINE)
		r = re.search(compiled_regex, string)
		
		# generate return mapping
		mappings: dict[str, str] = {}
		for var in variables_present:
			var_value = r.group(var)
			mappings[var] = var_value
		return mappings