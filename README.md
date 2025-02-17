# GitHub Repository Extractor

GitHub Repository Extractor is a Python-based tool designed to extract the file tree and content from a GitHub repository and format it in a way that's ideal for pasting into LLM (Large Language Model) prompts. This tool clones the repository, builds a visual file tree, and processes each file—excluding configuration files like `.env`, and documentation files such as `README` and `prerequistes`.

## Features

- **Repository Cloning:** Clones a given GitHub repository into a temporary folder.
- **File Tree Generation:** Recursively generates a visual representation of the repository's structure.
- **Content Extraction:** Reads and formats the content of each file, excluding specific files (e.g., `.env`, `README`, and `prerequistes`).
- **LLM-Ready Format:** Outputs the extracted data in a format that can be easily pasted into LLM models.
- **GUI Interface:** Provides a Tkinter-based GUI with:
  - An input field for the GitHub repository URL.
  - An "Extract" button to start the extraction process.
  - A text area to display the formatted output.
  - "Copy" and "Clear" buttons below the text area to manage the output.

## Installation

### Prerequisites

- **Python 3.x** installed on your system.
- **Git** must be installed and accessible from your command line.
- Required Python packages:
  - `pyperclip`
  - `tkinter` (usually comes with Python)
  
You can install the required Python packages using pip:

```bash
pip install pyperclip
