from src.writers.bibtex_writer import BibtexWriter
from src.binding.binder_options import BinderOptions
from src.publications.publication_binder import PublicationBinder
from src.publications.extract_publications import ExtractPublications
from src.publications.publication import Publication
from src.files import Files
import argparse

OPTIONS_ARG_NAME = "options"
OUT_ARG_NAME = "out"
IN_ARG_NAME = "in"
EXTRACT_ARG_NAME = "extract-dir"
SKIP_EXTRACT_ARG_NAME = "skip-extract"
IN_ENC_ARG = "input-encoding"
OUT_ENC_ARG = "output-encoding"

def parse_args() -> argparse.Namespace:
	parser = argparse.ArgumentParser(prog="RegBibEx (RBX)",
		description="An HTML to BibTex extractor based on regular expressions")
	parser.add_argument("options", help="The options file to use. See README.md for structure.")
	parser.add_argument("-i", f"--{IN_ARG_NAME}", "--input", default="input/ucb_2024.htm", help="Input (HTML) file to extract.")
	parser.add_argument("-o", f"--{OUT_ARG_NAME}", default="out", help="Output directory for created BibTex files.")
	parser.add_argument("-xd", f"--{EXTRACT_ARG_NAME}", default="extract", help="Directory to write the per-publication-extracted HTML files.")
	parser.add_argument("-sx", f"--{SKIP_EXTRACT_ARG_NAME}", action="store_true", help="If this flag is set, extracting files will be skipped. Use if extracted texts are already present to save time.")
	parser.add_argument("-ie", f"--{IN_ENC_ARG}", default=None, help="Encoding of the input file.")
	parser.add_argument("-oe", f"--{OUT_ENC_ARG}", default="utf-8", help="Target encoding of the output file.")
	return parser.parse_args()

def run_main(args: argparse.Namespace):
	varargs = vars(args)
	option_file = varargs[OPTIONS_ARG_NAME.replace("-", "_")]
	input_file = varargs[IN_ARG_NAME.replace("-", "_")]
	extract_output_dir = varargs[EXTRACT_ARG_NAME.replace("-", "_")]
	bibtex_output_dir = varargs[OUT_ARG_NAME.replace("-", "_")]
	skip_extract_and_convert = varargs[SKIP_EXTRACT_ARG_NAME.replace("-", "_")]
	in_encoding = varargs[IN_ENC_ARG.replace("-", "_")]
	out_encoding = varargs[OUT_ENC_ARG.replace("-", "_")]

	if (skip_extract_and_convert == False):
		# --- extract publications to own html
		print("extracting")
		input_file = ExtractPublications.extract_text(
			input_file, extract_output_dir, [1, 2], delete_existing=True)

		print("converting")
		# --- convert to utf-8
		for f in input_file:
			j = Publication(f, in_encoding)
			j.write_to_file(f, pretty=True, out_encoding=out_encoding)

		print("finished extracting and converting")

	# init options
	options = BinderOptions(option_file)

	# init filename to file map
	filename_to_file = {
		path_and_name[:path_and_name.rfind(".")].removeprefix(extract_output_dir + "\\"): path_and_name
		for path_and_name in input_file
	}

	# remove output directory
	Files.delete_folder(bibtex_output_dir)

	# do binding and write bibtex for each file defined in options
	for name in options.individual_opts.keys():
		if (name not in filename_to_file.keys()):
			continue
		
		file_path = filename_to_file[name]

		testpub = Publication(file_path, "utf-8")
		log_output = f"{bibtex_output_dir}/{name}"
		testpub_binder = PublicationBinder(testpub, options, log_output)
		btx = testpub_binder.get_bibtex()

		# --- write bibtex
		writer = BibtexWriter(bibtex_output_dir, options)
		writer.write_bibtex_to_file(testpub.get_filename(with_extension=False), btx)

	print("done")

def main():
	args = parse_args()
	run_main(args)

if __name__ == '__main__':
	main()
