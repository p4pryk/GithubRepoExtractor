import os
import tempfile
import shutil
import subprocess
import pyperclip
import tkinter as tk
from tkinter import scrolledtext, messagebox

def clone_github_repo(repo_url: str, target_dir: str) -> None:
    """
    Clones the GitHub repository into the specified directory.
    """
    try:
        subprocess.run(
            ["git", "clone", repo_url, target_dir],
            check=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE
        )
    except subprocess.CalledProcessError as e:
        raise Exception("Error cloning repository. Please ensure the URL is correct and that you have the necessary permissions.") from e

def get_all_files(directory: str) -> list:
    """
    Recursively obtains all file paths from the given directory,
    excluding files like '.env', files inside '.git' directories, 
    and files that start with 'README' or 'prerequistes' (case-insensitive).
    """
    file_paths = []
    for root, dirs, files in os.walk(directory):
        # Skip any .git directories
        dirs[:] = [d for d in dirs if d != '.git']
        for file in files:
            # Skip .env and files starting with README or prerequistes (case-insensitive)
            if file == '.env':
                continue
            if file.lower().startswith("readme.md") or file.lower().startswith("requirements.txt"):
                continue
            if file.lower().startswith("."):
                continue
            file_paths.append(os.path.join(root, file))
    return file_paths

def format_file_content(file_path: str, repo_root: str) -> str:
    """
    Reads and formats the content of a file. The file name is shown relative
    to the repository root.
    """
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            content = f.read()
    except Exception as e:
        content = f"Error reading file: {e}"
    relative_path = os.path.relpath(file_path, repo_root)
    return f"<{relative_path}>\n{content}\n</{relative_path}>"

def build_file_tree(directory: str, prefix="") -> str:
    """
    Recursively builds a visual representation of the file tree,
    skipping folders/files such as '.git' or '.env'.
    """
    tree_str = ""
    try:
        items = sorted(os.listdir(directory))
    except Exception:
        return tree_str
    # Filter out .git and .env
    items = [item for item in items if item not in ['.git', '.env']]
    for i, item in enumerate(items):
        full_path = os.path.join(directory, item)
        connector = "└── " if i == len(items) - 1 else "├── "
        tree_str += prefix + connector + item + "\n"
        if os.path.isdir(full_path):
            extension = "    " if i == len(items) - 1 else "│   "
            tree_str += build_file_tree(full_path, prefix + extension)
    return tree_str

def extract_repo_contents(repo_url: str) -> str:
    """
    Clones the repository, builds the file tree, formats the file contents,
    and then cleans up.
    """
    temp_dir = tempfile.mkdtemp()
    output_parts = []
    try:
        # Clone repository into temporary folder
        clone_github_repo(repo_url, temp_dir)

        # Build file tree representation
        file_tree = build_file_tree(temp_dir)
        output_parts.append("File Tree:")
        output_parts.append(file_tree)
        output_parts.append("-" * 40)

        # Process and format each file
        all_files = get_all_files(temp_dir)
        for file_path in all_files:
            formatted = format_file_content(file_path, temp_dir)
            output_parts.append(formatted)
    finally:
        # Clean up the cloned repository
        shutil.rmtree(temp_dir)
    final_output = "\n".join(output_parts)
    return final_output

def on_extract():
    """
    Triggered by the Extract button. Reads the GitHub URL, processes the repository,
    and updates the text area with the formatted output.
    """
    repo_url = entry_repo.get().strip()
    if not repo_url:
        messagebox.showerror("Error", "Please enter a valid GitHub repository URL.")
        return

    text_output.delete(1.0, tk.END)
    text_output.insert(tk.END, "Processing repository. Please wait...\n")
    root.update()
    try:
        final_output = extract_repo_contents(repo_url)
        text_output.delete(1.0, tk.END)
        text_output.insert(tk.END, final_output)
    except Exception as e:
        text_output.delete(1.0, tk.END)
        text_output.insert(tk.END, f"An error occurred:\n{e}")
        messagebox.showerror("Error", f"An error occurred: {e}")

def on_copy():
    """
    Copies the text from the output text box to the clipboard.
    """
    output = text_output.get(1.0, tk.END)
    pyperclip.copy(output)
    messagebox.showinfo("Copied", "Text has been copied to the clipboard!")

def on_clear():
    """
    Clears the text in the output text box.
    """
    text_output.delete(1.0, tk.END)

# ------------------------------
# Build the GUI
# ------------------------------

root = tk.Tk()
root.title("GitHub Repository Extractor")
root.geometry("800x650")

# Frame for title, description, and URL input
frame_top = tk.Frame(root)
frame_top.pack(padx=10, pady=10, fill=tk.X)

label_title = tk.Label(frame_top, text="GitHub Repository Extractor", font=("Helvetica", 16, "bold"))
label_title.pack(pady=5)

label_desc = tk.Label(
    frame_top,
    text=("Enter the URL of a GitHub repository below to extract and format its contents.\n"
          "This tool is especially useful when preparing text for LLM models by allowing you to paste\n"
          "the file tree and file contents directly into your prompt."),
    font=("Helvetica", 10)
)
label_desc.pack(pady=5)

entry_repo = tk.Entry(frame_top, width=80)
entry_repo.pack(pady=5)
entry_repo.insert(0, "https://github.com/username/repository.git")

button_extract = tk.Button(frame_top, text="Extract", command=on_extract)
button_extract.pack(pady=5)

# Scrolled text widget to display the final output
text_output = scrolledtext.ScrolledText(root, wrap=tk.WORD, width=100, height=30)
text_output.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)

# Frame for Copy and Clear buttons under the text box
frame_bottom = tk.Frame(root)
frame_bottom.pack(padx=10, pady=5)

button_copy = tk.Button(frame_bottom, text="Copy", command=on_copy)
button_copy.pack(side=tk.LEFT, padx=5)

button_clear = tk.Button(frame_bottom, text="Clear", command=on_clear)
button_clear.pack(side=tk.LEFT, padx=5)

root.mainloop()
