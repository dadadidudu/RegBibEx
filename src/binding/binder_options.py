from ..options.a_options import AOptions

class BinderOptions(AOptions):
	def __init__(self, options_file: str):
		super().__init__(options_file)