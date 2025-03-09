from src.publications.bibtex_writer import BibtexWriter
from src.binding.binder_options import BinderOptions
from src.publications.publication_binder import PublicationBinder
from src.binding.regex_variable_binder import RegexVariableBinder
from src.publications.extract_publications import ExtractPublications
from src.publications.publication import Publication

files = "./input/ucb_2024.htm"
journals_output_dir = "journals"
bibtex_output_dir = "bibtex"
test_publication = f"{journals_output_dir}/4.html"
bibtex_output_dir = "out"

# --- extract publications to own html
# print("extracting")
# files = ExtractPublications.extract_text(
#     files, journals_output_dir, [1, 2], delete_existing=True)

# # --- convert to utf-8
# for f in files:
# 	j = Publication(f)
# 	j.write_to_file(f, pretty=True, out_encoding="utf-8")

# --- test publication binder
options = BinderOptions("binding_prototype.txt")
testpub = Publication(test_publication, "utf-8")
testpub_binder = PublicationBinder(testpub, options)
btx = testpub_binder.get_bibtex()

# --- test bibtex writing
writer = BibtexWriter(bibtex_output_dir, options)
writer.write_bibtex_to_file(testpub.get_filename(with_extension=False), btx)

print("done")
