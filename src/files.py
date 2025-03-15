import os

class Files:
	@staticmethod
	def delete_folder(path: str) -> None:
		"Deletes the given path and all its subfiles and subfolders."

		if os.path.exists(path) == False:
			return
		for root, dirs, files, in os.walk(path):
			for f in files:
				filepath = os.path.join(root, f)
				os.remove(filepath)
		os.removedirs(path)
		print(f"removed {path}")
		
	@staticmethod
	def write_file(path: str, name: str, content: str, encoding = "utf-8") -> None:
		"Writes the given content to a new file with the given path and name. Path can be ommitted"

		if (path != ""):
			os.makedirs(path, exist_ok=True)
			with open(f"{path}/{name}", "w") as f:
				f.write(content)
		else:
			with open(f"{name}", "w", encoding=encoding) as f:
				f.write(content)
	
	@staticmethod
	def create_dir(dir: str) -> None:
		"If not existing, creates the given directory / directories."

		if (os.path.isdir(dir) is False):
			os.makedirs(dir)