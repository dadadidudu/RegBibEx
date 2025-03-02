from src.binding.binder_options import BinderOptions
from src.publications.publication_binder import PublicationBinder
from src.binding.regex_variable_binder import RegexVariableBinder
from src.publications.extract_publications import ExtractPublications
from src.publications.publication import Publication

files = "./input/ucb_2024.htm"
output_dir = "journals"
# --- extract publications to own html
print("extracting")
files = ExtractPublications.extract_text(
    files, output_dir, [1, 2], delete_existing=True)
# --- convert to utf-8 for readability (only for debugging!)
for f in files:
	j = Publication(f)
	j.write_to_file(f.replace(".html", ".conv.html"))
# --- test output
testfile = [x for x in files if "\\10.html" in x][0]
j = Publication(testfile)
print(j.as_htmltext())

# --- test publication get text
j = Publication(f"{output_dir}/4.conv.html")
jc = j.get_text_at("p.span")
print(jc)

# --- test binding
a = RegexVariableBinder(optionsfile="binding_prototype.txt")

bla0 = a.apply(jc[0], r"\d. {{TITLE}} ([–-]?) ?{{.*? as ORT}}, {{\d{4} as JAHR}}")
bla1 = a.apply(jc[1], r"\d. {{TITLE}} ([–-]?) ?{{.*? as ORT}}, {{\d{4} as JAHR}}")
bla2 = a.apply(jc[2], r"\d. {{TITLE}} ([–-]?) ?{{.*? as ORT}}, {{\d{4} as JAHR}}")
print(bla0)
print(bla1)
print(bla2)

# --- test publication binder#
opts = BinderOptions("binding_prototype.txt")
j2 = Publication(f"{output_dir}/4.conv.html")
jb = PublicationBinder(j, opts)
jb.get_bibtex()

print("done")
