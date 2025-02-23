from src.encoding import convert_to_utf8
from src.extract_journals import ExtractJournals
from src.journal import Journal

files = "./input/ucb_2024.htm"
output_dir = "journals"
print("extracting")
files = ExtractJournals.extract_text(
    files, output_dir, [1, 2], delete_existing=True)

for f in files:
	j = Journal(f)
	j.write_to_file(f.replace(".html", ".conv.html"))

testfile = [x for x in files if "\\10.html" in x][0]
j = Journal(testfile)

print(j.as_htmltext())

print("done")
