from .binding.binder_options import BinderOptions
from .binding.regex_variable_binder import RegexVariableBinder
from .journal import Journal
import os.path as path

class JournalBinder:

	journal: Journal
	binder: RegexVariableBinder
	options: BinderOptions

	def __init__(self, journal: Journal, options: BinderOptions):
		self.journal = journal
		self.options = options
		self.binder = RegexVariableBinder(binderoptions=options)
	
	def get_options_for_file(self) -> dict[str,str] | None:
		filename = path.basename(self.journal.file)
		last_dot_idx = filename.rfind(".")
		filename = filename[0:last_dot_idx]
		opts_for_file = self.options.get_individual_options(filename)
		return opts_for_file

