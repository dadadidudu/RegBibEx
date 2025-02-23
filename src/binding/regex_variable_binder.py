import re
from .binder_options import BinderOptions

KEYWORD_VARIABLE_DEFINITION = " as " # {{REGEX as VARIABLE}}

class RegexVariableBinder:
	"""
	Binds variables defined in RegularExpressions as python variables.
	E.g.: \d.: {{TITLE}}, {{\d{4} as YEAR}} will bind the contents of the string "1.: My Film Title, 1999" to the specified variables: TITLE: "My Film Title", YEAR: "1999".
	"""

	options: BinderOptions
	variables: dict[str, str]
	variable_finder_pattern: re.Pattern

	def __init__(self, optionsfile: str = "", binderoptions: BinderOptions = None):
		"""
		Suppy either a path to an options file for the binder, or already existing BinderOptions to be used for this Binder. If none are supplied, only {{REGEX as VARIABLE}} definitions will work.
		"""
		if (optionsfile != ""):
			self.options = BinderOptions(optionsfile)
		elif (binderoptions is not None):
			self.options = BinderOptions(binderoptions)
		else:
			print(r"RegexVariableBinder initialised without any options. Only {{REGEX as VARIABLE}} definitions possible.")
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
				if (self.options is not None):
					variable = var
					regex = self.options.defaults[var]
				else:
					raise r"Cannot use RegexVariableBinder with {{VARIABLE}} syntax: Options are missing."

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