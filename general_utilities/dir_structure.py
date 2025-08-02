import os

def generate_tree_structure(root_dir, output_file="dir_structure.txt"):
    def tree(dir_path, prefix=""):
        entries = sorted(os.listdir(dir_path))

        entries = [
            e for e in entries
            if not e.startswith('.') and e != '__pycache__' and e != output_file
        ]

        result = []
        for index, entry in enumerate(entries):
            path = os.path.join(dir_path, entry)
            connector = "├── " if index < len(entries) - 1 else "└── "
            result.append(f"{prefix}{connector}{entry}")
            if os.path.isdir(path):
                extension = "│   " if index < len(entries) - 1 else "    "
                result.extend(tree(path, prefix + extension))
        return result

    structure = [os.path.basename(os.path.abspath(root_dir)) + "/"]
    structure += tree(root_dir)

    with open(output_file, "w", encoding="utf-8") as f:
        f.write("\n".join(structure))
    print(f"Directory structure saved to {output_file}")

# Run from the root of your project
if __name__ == "__main__":
    generate_tree_structure(os.getcwd())
