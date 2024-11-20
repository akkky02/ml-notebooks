import nbformat


def create_collapsible_answer_cell(code):
    # Function to create a collapsible cell containing the original code
    collapsible_code = f"""
<details>
<summary>Click to expand code</summary>

```python
{code}
"""
    return nbformat.v4.new_markdown_cell(collapsible_code)


def clear_code_and_add_answers(nb_path, output_path):
    # Load the notebook
    with open(nb_path, "r", encoding="utf-8") as f:
        nb = nbformat.read(f, as_version=4)
    new_cells = []

    for cell in nb.cells:
        if cell.cell_type == "code":
            # Split the source code by lines
            lines = cell.source.split("\n")
            # Keep only the comment lines
            comments = [line for line in lines if line.strip().startswith("#")]
            # Join the comments back together
            comment_str = "\n".join(comments)

            # Create a new markdown cell with comments
            if comment_str.strip():  # Only add if there are comments
                new_cells.append(nbformat.v4.new_code_cell(comment_str))

            # Create a collapsible markdown cell with the original code
            new_cells.append(create_collapsible_answer_cell(cell.source))
        else:
            new_cells.append(cell)

    nb.cells = new_cells

    # Write the modified notebook to a new file
    with open(output_path, "w", encoding="utf-8") as f:
        nbformat.write(nb, f)


clear_code_and_add_answers(
    "1_PyTorchTensors.ipynb", "1_PyTorchTensors_collapsible.ipynb"
)
