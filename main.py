from src.binding.binder import Binder
from src.extract_journals import ExtractJournals
from src.journal import Journal

files = "./input/ucb_2024.htm"
output_dir = "journals"
# # --- extract journals to own html
# print("extracting")
# files = ExtractJournals.extract_text(
#     files, output_dir, [1, 2], delete_existing=True)
# # --- convert to utf-8 for readability
# for f in files:
# 	j = Journal(f)
# 	j.write_to_file(f.replace(".html", ".conv.html"))
# # --- test output
# testfile = [x for x in files if "\\10.html" in x][0]
# j = Journal(testfile)
# print(j.as_htmltext())

# --- test binding
a = Binder("binding_prototype.txt")
j = Journal("journals/4.conv.html")
s = [
	"1. Das sprachliche Bild der Bernsteinstraße-Region – Szombathely, 1994",
	"2. SCLOMB (Studia Comparativa Linguarum Orbis Maris Baltici) und Mittel-Europa -Szombathely, 1996",
	"3. János Rechnitzer: Die Charakteristiken des Übergangs in der Regionalstruktur Ungarns – Szombathely, 1999"
]

bla0 = a.apply(s[0], r"\d. {{TITLE}} ([–-]) ?{{.* as ORT}}, {{\d{4} as JAHR}}")
bla1 = a.apply(s[1], r"\d. {{TITLE}} ([–-]) ?{{.* as ORT}}, {{\d{4} as JAHR}}")
bla2 = a.apply(s[2], r"\d. {{TITLE}} ([–-]) ?{{.* as ORT}}, {{\d{4} as JAHR}}")

print("done")
