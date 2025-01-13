import re, os
from bs4 import BeautifulSoup, Tag

def as_html(title, body):
	return f"""
<!DOCTYPE html>
<html>
<head>
<title>{title}</title>
</head>
<body>
{body}
</body>
</html>
"""

class ExtractJournals:
	@staticmethod
	def extract_html(html_file_path: str, output_path: str):
		html = None
		with open(html_file_path) as file:
			content = file.read()
			html = BeautifulSoup(content, features="lxml")
		body: Tag = html.body # type: ignore
		all_headers = body.find_all("h1")
		for h1 in all_headers:
			pass
		pass

	@staticmethod
	def extract_text(input_file: str, output_path: str):
		body: str = ""

		# read html file and extract body
		with open(input_file) as file:
			content = file.read()
			body = ExtractJournals.get_text_between_tags("div", content)
		
		# find all h1 and write them as seperate html files
		startpos = -1
		endpos = -1
		title = "asd"
		num_h1 = sum(1 for _ in re.finditer("<h1", body))
		curr_match = 1
		for match in re.finditer("<h1", body):
			startpos = endpos
			endpos = match.span()[0]
			if startpos == -1:
				# first: skip (no endpos)
				continue
			else:
				content = body[startpos:endpos-1]
				# surround with html tags
				ExtractJournals.write_file(output_path, f"{curr_match}.html", as_html(title=title, body=content))
			
			if curr_match + 1 == num_h1:
				# last: 
				content = body[endpos:]
				ExtractJournals.write_file(output_path, f"{curr_match + 1}.html", as_html(title=title, body=content))

			curr_match += 1
		pass

	@staticmethod
	def write_file(path: str, name:str, content: str):
		os.makedirs(path, exist_ok=True)
		with open(f"{path}/{name}", "w") as f:
			f.write(content)

	@staticmethod
	def get_text_between_tags(tag: str, content: str):
		start = content.find(f"<{tag}")
		end = content.rfind(f"</{tag}>") + len(f"</{tag}>")
		text = content[start:end]
		return text