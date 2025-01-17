from src.encoding import convert_to_utf8
from src.extract_journals import ExtractJournals
import os

files = "./input/ucb_2024.htm"
output_dir = "journals"
print("extracting")
ExtractJournals.extract_text(files, output_dir, [1, 2], delete_existing=True)

print("converting to utf-8")

# for root, _, files in os.walk(output_dir):
#     for f in files:
#         convert_to_utf8.convert_to_utf8(os.path.join(root, f))

print("done")
