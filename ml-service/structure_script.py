import os


def generate_tree(startpath, exclude_dirs=None):
    if exclude_dirs is None:
        exclude_dirs = {'.git', '__pycache__', 'venv', '.vscode', '.idea', '.venv'}

    tree_lines = []
    for root, dirs, files in os.walk(startpath):
        # Filter out excluded directories in-place
        dirs[:] = [d for d in dirs if d not in exclude_dirs]

        level = root.replace(startpath, '').count(os.sep)
        indent = '│   ' * (level)
        sub_indent = '├── ' if level > 0 else ''

        # Add the directory name
        if level == 0:
            tree_lines.append(f"{os.path.basename(root)}/")
        else:
            tree_lines.append(
                f"{indent[:-4]}└── {os.path.basename(root)}/" if not dirs and not files else f"{indent[:-4]}├── {os.path.basename(root)}/")

        # Add files
        sub_indent = '│   ' * (level + 1)
        for i, f in enumerate(files):
            connector = '└── ' if i == len(files) - 1 else '├── '
            tree_lines.append(f"{sub_indent[:-4]}{connector}{f}")

    return "\n".join(tree_lines)


def save_to_md(tree_text, output_file="project_structure.md"):
    with open(output_file, "w", encoding="utf-8") as f:
        f.write("# Project Structure\n\n")
        f.write("```text\n")
        f.write(tree_text)
        f.write("\n```")
    print(f"Structure saved to {output_file}")


if __name__ == "__main__":
    project_path = "."  # Current directory
    structure = generate_tree(project_path)
    save_to_md(structure)
