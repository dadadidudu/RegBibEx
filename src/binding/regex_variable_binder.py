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
			options = BinderOptions(binderoptions)
			self.defaults = options.defaults
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
		for varDef in re.findall(self.variable_finder_pattern, regex_with_bindings):
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
			regex_with_bindings = regex_with_bindings.replace(r"{{" + varDef + r"}}", new)
		
		# apply the converted regex
		compiled_regex = re.compile(regex_with_bindings, re.MULTILINE)
		r = re.search(compiled_regex, string)
		if (r is None):
			raise Exception("Regex yielded no results")
		
		# generate return mapping
		mappings: dict[str, str] = {}
		for varDef in variables_present:
			var_value = r.group(varDef)
			mappings[varDef] = var_value

		return mappings