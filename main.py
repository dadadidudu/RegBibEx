from src.extract_journals import ExtractJournals

file = "./input/ucb_2024.htm"
ExtractJournals.extract_text(file, "journals")
print("done")
