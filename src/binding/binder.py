from .options.binding_options import BindingOptions

class Binder:

	options: BindingOptions

	def __init__(self, optionsfile: str):
		self.options = BindingOptions(optionsfile)