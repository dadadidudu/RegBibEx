__version__ = "1.1.0"

from src.writers.bibtex_writer import BibtexWriter
from src.binding.binder_options import BinderOptions
from src.publications.publication_binder import PublicationBinder
from src.publications.extract_publications import ExtractPublications
from src.publications.publication import Publication
from src.files import Files
import os
import argparse

OPTIONS_ARG_NAME = "options"
OUT_ARG_NAME = "output"
IN_ARG_NAME = "input"
EXTRACT_ARG_NAME = "extract-dir"
SKIP_EXTRACT_ARG_NAME = "skip-extract"
IN_ENC_ARG = "input-encoding"
EXTRACT_ENC_ARG = "extract-encoding"

def parse_args() -> argparse.Namespace:
	parser = argparse.ArgumentParser(prog="RegBibEx (RBX)",
		description="An HTML to BibTex extractor based on regular expressions")
	parser.add_argument("options", help="The options file to use. See README.md for structure.")
	parser.add_argument("-i", f"--{IN_ARG_NAME}", "--in", default="input/ucb_2024.htm", help="Input (HTML) file to extract. Default:\"input/ucb_2024.htm\"")
	parser.add_argument("-o", f"--{OUT_ARG_NAME}", "--out", default="out", help="Output directory for created BibTex files. Default:\"out\"")
	parser.add_argument("-xd", f"--{EXTRACT_ARG_NAME}", default="extract", help="Directory to write the per-publication-extracted HTML files. Default: \"extract\"")
	parser.add_argument("-sx", f"--{SKIP_EXTRACT_ARG_NAME}", action="store_true", help=f"If this flag is set, extracting files will be skipped. Use if extracted texts are already present in the directory given with -xd/--{EXTRACT_ARG_NAME} to save time on later script runs.")
	parser.add_argument("-ie", f"--{IN_ENC_ARG}", default=None, help="Encoding of the HMTL input file. Default: unspecified")
	parser.add_argument("-xe", f"--{EXTRACT_ENC_ARG}", default="utf-8", help=f"Target encoding of the extraction output file(s). Note: If the flag '-sx/--{SKIP_EXTRACT_ARG_NAME}' is supplied, this will be the encoding with which the binding input files will be read. Default:\"utf-8\"")
	parser.add_argument("--version", action="version", version=f"%(prog)s : Version {__version__}")
	return parser.parse_args()

def run_main(args: argparse.Namespace):
	varargs = vars(args)
	option_file = varargs[OPTIONS_ARG_NAME.replace("-", "_")]
	input_file = varargs[IN_ARG_NAME.replace("-", "_")]
	extract_output_dir = varargs[EXTRACT_ARG_NAME.replace("-", "_")]
	bibtex_output_dir = varargs[OUT_ARG_NAME.replace("-", "_")]
	skip_extract_and_convert = varargs[SKIP_EXTRACT_ARG_NAME.replace("-", "_")]
	in_encoding = varargs[IN_ENC_ARG.replace("-", "_")]
	extractfiles_encoding = varargs[EXTRACT_ENC_ARG.replace("-", "_")]

	extracted_files: list[str] = []

	if (skip_extract_and_convert == False):
		# --- extract publications to own html
		print("extracting")
		extracted_files = ExtractPublications.extract_text(
			input_file, extract_output_dir, [1, 2], delete_existing=True)

		print("converting")
		# --- convert to utf-8
		for f in extracted_files:
			j = Publication(f, in_encoding)
			j.write_to_file(f, pretty=True, out_encoding=extractfiles_encoding)

		print("finished extracting and converting")
	else:
		if (extract_output_dir is not None and extract_output_dir != ""):
			# get all files only in extract directory
			extracted_files = [os.path.join(extract_output_dir, f) for f in os.listdir(extract_output_dir)]
			extracted_files = [f for f in extracted_files if os.path.isfile(f)]
		else:
			raise Exception("Invalid extract directory")

	# init options
	options = BinderOptions(option_file)

	# init filename to file map
	filename_to_file = {
		os.path.splitext(os.path.basename(path_and_name))[0]: path_and_name
		for path_and_name in extracted_files
	}

	# remove output directory
	Files.delete_folder(bibtex_output_dir)

	# do binding and write bibtex for each file defined in options
	for name in options.individual_opts.keys():
		if (name not in filename_to_file.keys()):
			continue
		
		file_path = filename_to_file[name]

		publication = Publication(file_path, extractfiles_encoding) # utf-8 hardcoded here as we're using it internally as "working encoding", maybe change?
		log_output = f"{bibtex_output_dir}/{name}"
		testpub_binder = PublicationBinder(publication, options, log_output)
		btx = testpub_binder.get_bibtex()

		# --- write bibtex
		writer = BibtexWriter(bibtex_output_dir, options)
		writer.write_bibtex_to_file(publication.get_filename(with_extension=False), btx)

	print("done")

def main():
	args = parse_args()
	run_main(args)

if __name__ == "__main__":
	main()
