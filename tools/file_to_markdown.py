from pathlib import Path
from markitdown import MarkItDown

input_path = Path("../raw/")  # add files in raw/ to convert into .md format
output_path = input_path.with_suffix(".md")

# create md
md = MarkItDown(enable_plugins=False)
result = md.convert(str(input_path))

# save
output_path.write_text(result.text_content, encoding="utf-8")

print(f"Successfully converted '{input_path.name}' to '{output_path.name}'")