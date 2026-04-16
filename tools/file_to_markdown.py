import argparse
from tqdm import tqdm
from pathlib import Path
from markitdown import MarkItDown


def convert_directory_to_md(input_dir: Path):
    """
    Converts all files in a dictory to a Markdown format. Original files in the folder will be deleted.
    :param input_dir:
        The Path object pointing to the directory to process.
    """

    md = MarkItDown(enable_plugins=False)

    # get list of files to convert
    files_to_process = [f for f in input_dir.iterdir() if f.is_file()]
    total = len(files_to_process)

    if not files_to_process:
        print(f"No files found in {input_dir}!")
        return

    for file_path in tqdm(files_to_process, desc="Converting Files"):
        # skip .ds and .gitkeep files
        if file_path.suffix in ['.ds', '.gitkeep']:
            tqdm.write(f"Ignoring '.ds' and '.gitkeep': {file_path.name}")
            continue

        # convert filepath to md
        output_path = file_path.with_suffix(".md")
        try:
            # convert
            result = md.convert(str(file_path))
            # save to .md
            output_path.write_text(result.text_content, encoding="utf-8")
            # remove original file
            file_path.unlink()
            tqdm.write(f"Converted: {file_path.name}")
        except Exception:
            tqdm.write(f"FAILED: Could not convert '{file_path.name}'. Skipping.")


def main(args):
    # set Paths
    input_path = Path(args.input_dir).resolve()
    print("-" * 40)
    print(f"Input Directory: {input_path}")
    print("-" * 40)

    # execute
    try:
        convert_directory_to_md(input_path)
        print("\nConversion process complete.")
    except FileNotFoundError:
        print(f"\nError: Input directory not found at {input_path}")
    except Exception as e:
        print(f"\nAn unexpected error occurred during execution: {e}")


if __name__ == "__main__":
    """Command-line arguments."""
    parser = argparse.ArgumentParser(description="Convert all files in a directory to Markdown and delete originals.")
    parser.add_argument(
        "--input_dir",
        type=str,
        help="The path to the directory containing files to convert."
    )
    args = parser.parse_args()

    main(args)
