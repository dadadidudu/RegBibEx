from src.publications.bibtex_writer import BibtexWriter
from src.binding.binder_options import BinderOptions
from src.publications.publication_binder import PublicationBinder
from src.publications.extract_publications import ExtractPublications
from src.publications.publication import Publication
from src.files import Files

files = "./input/ucb_2024.htm"
extract_output_dir = "journals"
bibtex_output_dir = "out"

# --- extract publications to own html
print("extracting")
files = ExtractPublications.extract_text(
    files, extract_output_dir, [1, 2], delete_existing=True)

print("converting")
# --- convert to utf-8
for f in files:
	j = Publication(f)
	j.write_to_file(f, pretty=True, out_encoding="utf-8")

print("finished extracting and converting")

# init options
options = BinderOptions("binding_prototype.txt")

# init filename to file map
filename_to_file = {
	path_and_name[:path_and_name.rfind(".")].removeprefix(extract_output_dir + "\\"): path_and_name
	for path_and_name in files
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

# TODO: add file output (instead of console) unmapped and selection 