from src.binding.regex_variable_binder import RegexVariableBinder
from src.extract_journals import ExtractJournals
from src.journal import Journal

files = "./input/ucb_2024.htm"
output_dir = "journals"
# # --- extract journals to own html
# print("extracting")
# files = ExtractJournals.extract_text(
#     files, output_dir, [1, 2], delete_existing=True)
# # --- convert to utf-8 for readability (only for debugging!)
# for f in files:
# 	j = Journal(f)
# 	j.write_to_file(f.replace(".html", ".conv.html"))
# # --- test output
# testfile = [x for x in files if "\\10.html" in x][0]
# j = Journal(testfile)
# print(j.as_htmltext())

# --- test journal get text
j = Journal("journals/4.html")
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

print("done")
